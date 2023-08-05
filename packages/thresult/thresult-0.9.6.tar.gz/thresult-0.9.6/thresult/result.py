__all__ = ['ResultException', 'ResultType', 'Result', 'Ok', 'Err', 'wrap_result']

import asyncio
import types
from typing import Any, Callable
from inspect import iscoroutinefunction

class ResultException(BaseException):
    pass


class _ResultType(type):
    pass


class ResultType(_ResultType):
    def __getitem__(cls, key: Any) -> type:
        if cls is Ok or issubclass(cls, Ok):
            T: ResultType = type(f'Ok[{key}]', (Ok,), {
                '__annotations__': {
                    'v': key
                }
            })
        elif cls is Err or issubclass(cls, Err):
            T: ResultType = type(f'Err[{key}]', (Err,), {
                '__annotations__': {
                    'e': key
                }
            })
        elif cls is Result or issubclass(cls, Result):
            T: ResultType = type(f'Result[{key}]', (Result,), {
                '__annotations__': {
                    'v': key[0],
                    'e': key[1],
                }
            })
        else:
            raise TypeError(f'Unsupported type {cls}') # pragma: no cover

        return T


    def __or__(cls: type, other: type) -> 'ResultType':
        V: type = cls.__annotations__['v']
        E: type = other.__annotations__['e']

        T: ResultType = type(f'Result[{V}, {E}]', (Result,), {
            '__annotations__': {
                'v': V,
                'e': E,
            }
        })

        return T


    def __eq__(cls: type, other: type) -> bool:
        return (
            cls.__annotations__['v'] == other.__annotations__['v'] and
            cls.__annotations__['e'] == other.__annotations__['e']
        )


    def __call__(cls, *args, **kwargs) -> Callable:
        if (
            len(args) == 1 and
            not kwargs and
            not issubclass(cls, Ok) and
            not issubclass(cls, Err) and
            (fn := args[0]) and
            (callable(fn) or asyncio.iscoroutinefunction(fn))
        ):
            V = cls.__annotations__['v']
            E = cls.__annotations__['e']
            
            if asyncio.iscoroutinefunction(fn):
                async def wrap(*args, **kwargs) -> Any:
                    try:
                        v = await fn(*args, **kwargs)
                        return Ok[V](v)
                    except BaseException as e: #  TODO check it was Exception not BaseException
                        return Err[E](e)
            elif callable(fn):
                def wrap(*args, **kwargs) -> Any:
                    try:
                        v = fn(*args, **kwargs)
                        return Ok[V](v)
                    except BaseException as e: #  TODO check it was Exception not BaseException
                        return Err[E](e)

            return wrap
        else:
            return super().__call__(*args, **kwargs)


class _Result(metaclass=ResultType):
    v: type | None = None
    e: type | None = None


class Result(_Result):
    def __new__(cls, *args, **kwargs) -> None:
        raise TypeError('Cannot be instantiated')


class Ok(Result):
    __match_args__ = ('v',)
    v: Any


    def __new__(cls, *args, **kwargs) -> 'Ok':
        self = _Result.__new__(cls)
        return self


    def __init__(self, v: Any):
        V: type = self.__class__.__annotations__['v']

        if not (isinstance(V, types.GenericAlias)
                or isinstance(V, str)
                or V is Any
                or isinstance(v, V)):
            raise TypeError(f'Got {type(v)} but expected {self.__class__.__annotations__["v"]}')
        
        self.v = v


    def unwrap(self) -> Any:
        """
        This function unwrap and returns a value of Ok type of Result
        """
        return self.v


    def unwrap_or(self, v: Any) -> Any:
        """
        This function unwrap and returns a value of Ok type of Result
        """
        return self.v


    def unwrap_value(self) -> Any:
        """
        This function unwrap and returns a value of Ok type of Result
        """
        return self.v


class Err(Result):
    __match_args__ = ('e',)
    e: Any


    def __new__(cls, *args, **kwargs) -> 'Err':
        self = _Result.__new__(cls)
        return self


    def __init__(self, e: Any):
        E: type = self.__class__.__annotations__['e']

        if not (isinstance(E, types.GenericAlias)
                or isinstance(E, str)
                or E is Any
                or isinstance(e, (E, BaseException))):
            raise TypeError(f'Got {type(e)} but expected {self.__class__.__annotations__["e"]}')

        self.e = e


    def unwrap(self) -> None:
        """
        This function unwrap and raise exception of Error type of Err type of Result
        """
        if not isinstance(self.e, BaseException):
            e = ResultException(self.e)
        else:
            e = self.e # pragma: no cover

        raise e


    def unwrap_or(self, v: Any) -> Any:
        """
        This function unwrap and returns a value
        """
        return v


    def unwrap_value(self) -> Any:
        """
        This function unwrap and returns a value of Err type of Result
        """
        return self.e


def wrap_result(res: Result):
    """
    This function wraps the Result type and returns a Ok or Err type of Result
    """
    def outer(f):
        def inner(*args, **kwargs):
            if iscoroutinefunction(f):
                async def a():
                    try:
                        v = await f(*args, **kwargs)
                        return Ok(v)
                    except BaseException as e: #  TODO check it was Exception not BaseException
                        return Err(e)  
                return a()
            else:
                try:
                    v = f(*args, **kwargs)
                    return Ok(v)
                except BaseException as e: #  TODO check it was Exception not BaseException
                    return Err(e)

        return inner

    return outer

