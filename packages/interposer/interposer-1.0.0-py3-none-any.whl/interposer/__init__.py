# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 - 2020 Tuono, Inc.
# Copyright (C) 2021 - 2022 CloudTruth, Inc.
#
import inspect

from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

from wrapt import CallableObjectProxy


@dataclass
class CallBypass:
    """
    Provides an alternate result to a call.
    """

    result: Any


@dataclass
class CallContext:
    """
    Provides argument and temporary storage for the call duration.

    Attributes:
        call (Callable): the entity called
        args (tuple): the call arguments
        kwargs (dict): the call keyword arguments
        meta (dict): temporary storage for the duration of the call
                     that can be used by implementations to pass data
                     between begin and end call handling, also used to
                     affect behavior of certian call handlers

        rewrap (bool): used to control whether the result is rewrapped
                       this implements selective diving
    """

    call: Callable
    args: Tuple[Any]
    kwargs: Dict[str, Any]
    meta: Dict[str, Any] = field(default_factory=dict)

    @property
    def rewrap(self) -> bool:
        return self.meta.get("_flags", {}).get("rewrap", False)

    @rewrap.setter
    def rewrap(self, value: bool) -> None:
        self.meta.setdefault("_flags", {})["rewrap"] = value


class CallHandler(object):
    """
    Handles a call.
    """

    def on_call_begin(self, context: CallContext) -> Optional[CallBypass]:
        """
        Invoked on a call before the actual call is made.

        The args and kwargs are from the original caller so handle them with
        extreme care.  Modifying them will modify the caller's data!

        The implementation can bypass actual execution of the call by:
          1. Returning a CallBypass which contains a result to be returned
             to the caller, or
          2. Raising an exception.

        Returns:
          None, to proceed with the call.
          CallBypass, if the implementation wants to provide an alternate
            response and avoid the actual call all together.
        """
        pass

    def on_call_end_exception(
        self, context: CallContext, ex: Exception
    ) -> Optional[Exception]:
        """
        Invoked after the actual call is made if an exception occurred.

        If this method returns an Exception, it replaces the original
        exception.  If this method returns anything else, the original
        exception is maintained.

        If none of the call handlers replace the original
        exception then the framework will re-raise the original
        exception thus preserving the original error context.
        """
        return None

    def on_call_end_result(self, context: CallContext, result: Any) -> Any:
        """
        Invoked after the actual call is made if no exception occurred.

        In most cases whatever this method returns is returned to the caller
        which means implementations can modify the result.  If the result is
        the result of an object instantiation of class, the result is wrapped
        and then returned to the caller.
        """
        return result


class Interposer(CallableObjectProxy):
    """
    Wraps any class, object, method, or function allowing the method
    call/arguments and (result or exception raised) to be intercepted
    and modified.  Attribute lookups that fail on the interposer are
    handled by __getattr__ and satisfied by __wrapped__.

    Wrappable items do not include "primitives" - for example a string,
    int, bool, list, etc. as that would complicate a great many things
    including simple serialization.

    How it works:

    Loading an attribute (like `self.my_property`) will first check this
    class for that attribute, and if not found __getattr__ is called which
    will load the attribute from the wrapped entity.

    Making a call (like `self.my_call(foo)`) is actually loading an
    attribute (my_call) which is a method, then executing __call__ on it.
    The __call__ here intercepts that and allows for pre- and post- call
    behavior to be added.

    When a module is wrapped, the __getattr__ on the module to load
    either another module or a class is also wrapped.  This makes a child
    interposer around the class which is returned.

    When a class is wrapped, the result of the __call__ on the class
    to create an object is wrapped.  This makes a child interposer around
    the object which is returned.

    When an object is wrapped, any callable attribute retrieved through
    __getattr__ is also wrapped (typically, methods).  When a method is
    retrieved as part of a call sequence, this makes a child interposer
    around the method which is returned, then it gets __call__ed.

    When a method, function, built-in method, or built-in function is
    wrapped, the __call__ triggers on_call_begin before the actual call,
    and either on_call_result or on_call_exception after the call.
    Additionally, on_call_begin can cause result to be sent to the caller
    or raise an exception, bypassing the actual call completely.  This is
    useful when playing back responses that were recorded, for example.

    When subclassing to implement specific behavior, rememeber you must
    prefix _self_ in front of any class property you want to be able to
    access in your implementation due to wrapt.CallableObjectProxy rules.

    When stacking interposers (wrapping multiple times), the outer-most
    interposer intercepts first, and if it does not take terminal action,
    passes the call to the interposer it wrapped for additional processing.

    Finally, since the framework generates new interposers to maintain
    capture, any subclass must implement the capture method, allowing
    the framework to wrap and also allowing the subclass to optionally
    share state among the child interposers.
    """

    def __init__(
        self, entity: Any, handlers: Union[CallHandler, List[CallHandler]]
    ) -> None:
        """
        Wrap a module, class, object, method, or function and imbue calls
        with the behaviors of any CallHandler provided in the argument list.

        Args:
            entity (Any): A module, class, object, method, or function.
            handlers (list): Call handlers to invoke
        """
        super().__init__(entity)
        self._self_handlers = handlers if isinstance(handlers, list) else [handlers]

    def __call__(self, *args, **kwargs):
        """
        Handle a call on a wrapped callable.

        This means we've wrapped a class (when called makes an object) or
        that we've wrapped a method or function (when called returns a result).

        It is intentional that we are not logging anything here, as this
        information could contain secrets.
        """
        context = CallContext(self.__wrapped__, args, kwargs)

        # by default, a call to instantiate an object from a class definition
        # is rewrapped so we capture the calls on the object
        context.rewrap = inspect.isclass(self.__wrapped__)

        # see if a handler wants to bypass the call
        for handler in self._self_handlers:
            bypass = handler.on_call_begin(context)
            if bypass:
                if context.rewrap:
                    # FIXME: derived types cannot have additional arguments
                    return type(self)(bypass.result, self._self_handlers)
                else:
                    return bypass.result

        # nope, so make the actual call
        try:
            result = super().__call__(*context.args, **context.kwargs)
        except Exception as ex:
            orig_ex = ex
            for handler in self._self_handlers:
                repl = handler.on_call_end_exception(context, ex)
                if isinstance(repl, Exception):
                    ex = repl
            if ex is orig_ex:
                raise  # re-raise the original exception
            else:
                raise ex  # raise the replacement exception
        for handler in self._self_handlers:
            result = handler.on_call_end_result(context, result)

        if context.rewrap:
            # FIXME: derived types cannot have additional arguments
            result = type(self)(result, self._self_handlers)
        return result

    def __getattr__(self, name: str) -> Any:
        """
        Handle duck typing for the wrapped entity.

        If inspect says the attr has a module, which means it is not part of
        the python distribution (that is an assumption) then wrap it, because
        we want to wrap until we get to a __call__.  This allows top level
        objects that construct helpers as attributes (@property) to be
        captured properly.
        """
        attr = super().__getattr__(name)
        wrap = inspect.isbuiltin(attr) or inspect.getmodule(attr)
        if wrap:
            # FIXME: derived types cannot have additional arguments
            attr = type(self)(attr, self._self_handlers)
        return attr


def isinterposed(entity: Any) -> bool:
    """
    Checks to see if something is being interposed.
    """
    return type(entity) == Interposer
