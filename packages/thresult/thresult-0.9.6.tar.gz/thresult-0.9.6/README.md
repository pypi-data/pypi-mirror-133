[![Build][build-image]]()
[![Status][status-image]][pypi-project-url]
[![Stable Version][stable-ver-image]][pypi-project-url]
[![Coverage][coverage-image]]()
[![Python][python-ver-image]][pypi-project-url]
[![License][bsd3-image]][bsd3-url]


# thresult

## Overview
TangledHub library for handling returned values from functions/methods and handling errors.

## Licencing
thresult is licensed under the BSD license. Check the [LICENSE](https://opensource.org/licenses/BSD-3-Clause) for details

## Installation
```bash
pip install thresult
```

## Testing
```bash
docker-compose build thresult-test ; docker-compose run --rm thresult-test
```

## Building
```bash
docker-compose build thresult-build ; docker-compose run --rm thresult-build
```

## Publish
```bash
docker-compose build thresult-publish ; docker-compose run --rm -e PYPI_USERNAME=__token__ -e PYPI_PASSWORD=__SECRET__ thresult-publish
```

### Run examples from Docker
```bash
docker run -it -v $PWD/examples:/code -v $PWD:/deps/thresult -e PYTHONPATH=/deps python:3.10 /bin/bash
cd /code
python -B traceback_0.py
python -B traceback_1.py
python -B traceback_2.py
python -B traceback_3.py
```


## Usage
thresult provides type system for handling values and exceptions in Python.
Expressions can return value of type Result and variables can hold value of type Result.
Result can be Ok or Err. Ok type has attribute v and Err type has attribute e.
If some expression doesn't rise exception, it will return Ok type where v attribute will be result of expression.
If error occurs, Err type will be returned, and e attribute of that type will contain error message.
Custom types can be created, and they must extend Result, Ok or Err type.

Example when returned value is Ok type
```python
from thresult import Result, Ok, Err

def f(a: float, b: float) -> Result[float, Exception]:
    try:
        r: float = a / b
        res = Ok[float](r)
    except Exception as e:
        res = Err[Exception](e)
    
    return res

r: Result = f(1.0, 20.0) # r is Ok[<class 'float'>] object
```

Example when returned value is Err type
```python
from thresult import Result, Ok, Err

def f(a: float, b: float) -> Result[float, Exception]:
    try:
        r: float = a / b
        res = Ok[float](r)
    except Exception as e:
        res = Err[Exception](e)

    return res

# divide with 0.0 will not rise exception,
# object type Err[<class 'Exception'>] is returned
r: Result = f(1.0, 0.0) # r is Err[<class 'Exception'>] object
```

To obtain a value from Ok or Err type
- structural pattern matching
- unwrap()
- unwrap_value()
- unwrap_or(v: Any)

There are different ways to handle exceptions

Obtain a value from Ok or Err type 
with structural pattern matching
```python
from thresult import Result, Ok, Err

def f(a: float, b: float) -> Result[float, Exception]:
    try:
        r: float = a / b
        res = Ok[float](r)
    except Exception as e:
        res = Err[Exception](e)
    
    return res


r: Result = f(1.0, 0.0)

match r:
    case Ok(v):
        print('Ok, value: ', v)
    case Err(e):
        print('Err, error: ', e) # float division by zero
```

Using structural pattern matching to handle exceptions.
```python
from thresult import Result, Ok, Err


def f(a: float, b: float) -> Result[float, Exception]:
    try:
        r: float = a / b
        res = Ok[float](r)
    except Exception as e:
        res = Err[Exception](e)
    
    return res


match f(1.0, 0.0):
    case Ok(v):
        print('Ok, value: ', v)
    case Err(e):
        print('Err, error: ', e) # float division by zero
```

Using *unwrap* to handle exceptions.
In case of error, exception is thrown.
```python
from thresult import Result, Ok, Err

def f(a: float, b: float) -> Result[float, Exception]:
    try:
        r: float = a / b
        res = Ok[float](r)
    except Exception as e:
        res = Err[Exception](e)
    
    return res

r: Result = f(1.0, 0.0)
z: float = r.unwrap() # ZeroDivisionError: float division by zero
```

Using *unwrap_value* to handle exceptions.
In case of error, unwrap_value returns error message and doesn't terminate program.
```python
from thresult import Result, Ok, Err


def f(a: float, b: float) -> Result[float, Exception]:
    try:
        r: float = a / b
        res = Ok[float](r)
    except Exception as e:
        res = Err[Exception](e)
    
    return res


r: Result = f(1.0, 0.0)
v: str = r.unwrap_value()
# v will contain error message, float division by zero
```

Using *unwrap_or* to handle exceptions.
In case of error, unwrap_or returns value passed as argument and doesn't terminate program.
In this example it is 0.0.
```python
from thresult import Result, Ok, Err


def f(a: float, b: float) -> Result[float, Exception]:
    try:
        r: float = a / b
        res = Ok[float](r)
    except Exception as e:
        res = Err[Exception](e)
    
    return res


r: Result = f(1.0, 0.0)
v: float = r.unwrap_or(0.0)
# v will contain value 0.0
```

Obtain a value from Ok type using structural pattern matching.
```python
from thresult import Result, Ok, Err


def f(a: float, b: float) -> Result[float, Exception]:
    try:
        r: float = a / b
        res = Ok[float](r)
    except Exception as e:
        res = Err[Exception](e)
    
    return res


r: Result = f(1.0, 10.0)

match r:
    case Ok(v):
        # v holds value of division operation - 0.1
        print('Ok, value: ', v)
    case Err(e):
        print('Err, error: ', e)
```

Obtain a value from Ok type using structural pattern matching.
```python
from thresult import Result, Ok, Err


def f(a: float, b: float) -> Result[float, Exception]:
    try:
        r: float = a / b
        res = Ok[float](r)
    except Exception as e:
        res = Err[Exception](e)
    
    return res


match f(1.0, 10.0):
    case Ok(v):
        # v holds value of division operation - 0.1
        print('Ok, value: ', v)
    case Err(e):
        print('Err, error: ', e) 
```

Obtain a value from Ok type using *unwrap* method on variable.
Variable holds a value of Ok type.
```python
from thresult import Result, Ok, Err


def f(a: float, b: float) -> Result[float, Exception]:
    try:
        r: float = a / b
        res = Ok[float](r)
    except Exception as e:
        res = Err[Exception](e)
    
    return res


r: Result = f(1.0, 10.0)
v: float = r.unwrap() # v is 0.1
```

Obtain a value from Ok type using *unwrap* method on expression. 
Expression returns a value of Ok type.
```python
from thresult import Result, Ok, Err


def f(a: float, b: float) -> Result[float, Exception]:
    try:
        r: float = a / b
        res = Ok[float](r)
    except Exception as e:
        res = Err[Exception](e)
    
    return res


v: float = (f(1.0, 10.0)).unwrap() # v is 0.1
```


Obtain a value from Ok type using *unwrap_value* method on variable.
Variable holds a value of Ok type. If value is Ok type, *unwrap_value* has no effects, 
it is same as *unwrap* method.
```python
from thresult import Result, Ok, Err


def f(a: float, b: float) -> Result[float, Exception]:
    try:
        r: float = a / b
        res = Ok[float](r)
    except Exception as e:
        res = Err[Exception](e)
    
    return res

    
r: Result = f(1.0, 10.0)
v: float = r.unwrap_value() # v is 0.1
```

Obtain a value from Ok type using *unwrap* method on expression. 
Expression returns a value of Ok type. If value is Ok type, *unwrap_value* has no effects, 
it is same as *unwrap* method.
```python
from thresult import Result, Ok, Err


def f(a: float, b: float) -> Result[float, Exception]:
    try:
        r: float = a / b
        res = Ok[float](r)
    except Exception as e:
        res = Err[Exception](e)
    
    return res


v: float = (f(1.0, 10.0)).unwrap_value() # v is 0.1
```

Obtain a value from Ok type using *unwrap_or* method on variable.
Variable holds a value of Ok type. If value is Ok type, *unwrap_or* has no effects, 
it is same as *unwrap* or *unwrap_value* method.
```python
from thresult import Result, Ok, Err


def f(a: float, b: float) -> Result[float, Exception]:
    try:
        r: float = a / b
        res = Ok[float](r)
    except Exception as e:
        res = Err[Exception](e)
    
    return res


r: Result = f(1.0, 10.0)
v: float = r.unwrap_or(10.1) # v is 0.1
```

Obtain a value from Ok type using *unwrap_or* method on expression.
Expression returns a value of Ok type. If value is Ok type, *unwrap_or* has no effects, 
it is same as *unwrap* or *unwrap_value* method.
```python
from thresult import Result, Ok, Err


def f(a: float, b: float) -> Result[float, Exception]:
    try:
        r: float = a / b
        res = Ok[float](r)
    except Exception as e:
        res = Err[Exception](e)
    
    return res


v: float = (f(1.0, 10.0)).unwrap_or(10.1) # v is 0.1
```

thresult provides type checking
```python
from thresult import Result, Ok, Err


class A:
    pass

    
a = A()
at: Ok[A] = Ok[A](a) 
at: Ok[A] = Ok[A](4) # TypeError: Got <class 'int'> but expected <class 'A'>
```

create custom types by extending Ok and Err
```python
from thresult import Result, Ok, Err


class AOk(Ok):
    pass


class AErr(Err):
    pass


CustomResult: type = AOk[float] | AErr[str]


r: CustomResult = AOk[int](5)
v: int = r.unwrap_value() # v holds value of 5
```

Using decorators to obtain Ok type
```python
from thresult import Result, Ok, Err


@Result[float, str]
def f(n: float):
    return 1/n


v = f(10.0) # Ok[<class 'float'>]
f: float = v.unwrap() # 0.1
```

Using decorators to obtain Err type
```python
from thresult import Result, Ok, Err


@Result[float, str]
def f(n: float):
    return 1 / n


v = f(0.0)
m: str = v.unwrap_value() # float division by zero
```

Using decorators to obtain Ok 
Custom result type
```python
from thresult import Result, Ok, Err


# custom result type
CustomResult: type = Ok[float] | Err[str] 


@CustomResult[float, str]
def f(n: float):
    return 1 / n


v = f(10.0) # Ok[<class 'float'>]
f: float = v.unwrap() # 0.1
```

Using decorators to obtain Ok 
Custom result type
Using unwrap_value
```python
from thresult import Result, Ok, Err


# custom result type
CustomResult: type = Ok[float] | Err[str] 


@CustomResult[float, str]
def f(n: float):
    return 1 / n


v = f(10.0) # Ok[<class 'float'>]
f: float = v.unwrap_value() # 0.1
```

Using decorators to obtain Ok 
Custom result type
Using unwrap_or
```python
from thresult import Result, Ok, Err


# custom result type
CustomResult: type = Ok[float] | Err[str] 


@CustomResult[float, str]
def f(n: float):
    return 1 / n


v = f(10.0) # Ok[<class 'float'>]
f: float = v.unwrap_or(10.1) # 0.1
```

Using decorators to obtain Err 
Custom result type
```python
from thresult import Result, Ok, Err


CustomResult: type = Ok[float] | Err[str] 


@CustomResult[float, str]
def f(n: float):
    return 1 / n


v = f(0.0) # Err[<class 'str'>]
# panic: raising exception
f: float = v.unwrap() # ZeroDivisionError: float division by zero
```

Using decorators to obtain Err 
Custom result type
```python
from thresult import Result, Ok, Err


CustomResult: type = Ok[float] | Err[str] 


@CustomResult[float, str]
def f(n: float):
    return 1 / n


v = f(0.0) # Err[<class 'str'>]

# doesn't panic, returns exception's message as string
f: float = v.unwrap_value() # string value: float division by zero
```

Using decorators to obtain Err. 
Custom result type
Using unwrap_or()
```python
from thresult import Result, Ok, Err


CustomResult: type = Ok[float] | Err[str] 


@CustomResult[float, 'str']
def f(n: float):
    return 1 / n


v = f(0.0) # Err[<class 'str'>]

# doesn't panic, returns custom exception's message as string
f: float = v.unwrap_or('Zero division: Custom message') # string value: Zero division: Custom message 
```

Using decorators to obtain Ok.
Custom result type and custom Ok type
```python
from thresult import Result, Ok, Err


class CustomOk(Ok):
    pass

class CustomErr(Err):
    pass


CustomResult: type = CustomOk[float] | CustomErr[str] 


@CustomResult[float, str]
def f(n: float):
    return 1 / n


v = f(10.0) # Ok[<class 'float'>]
```

Using decorators to obtain Ok.
Custom result type and custom Ok type.
Obtain value with *unwrap*
```python
from thresult import Result, Ok, Err


class CustomOk(Ok):
    pass


class CustomErr(Err):
    pass


CustomResult: type = CustomOk[float] | CustomErr[str] 


@CustomResult[float, str]
def f(n: float):
    return 1 / n


v = f(10.0) # Ok[<class 'float'>]
r: float = v.unwrap() # 0.1
```

Using decorators to obtain Ok.
Custom result type and custom Ok type.
Obtain value with *unwrap_value*
```python
from thresult import Result, Ok, Err


class CustomOk(Ok):
    pass


class CustomErr(Err):
    pass


CustomResult: type = CustomOk[float] | CustomErr[str] 


@CustomResult[float, str]
def f(n: float):
    return 1 / n


v = f(10.0) # Ok[<class 'float'>]
r: float = v.unwrap_value() # 0.1
```

Using decorators to obtain Ok.
Custom result type and custom Ok type.
Obtain value with *unwrap_or*
```python
from thresult import Result, Ok, Err


class CustomOk(Ok):
    pass


class CustomErr(Err):
    pass


CustomResult: type = CustomOk[float] | CustomErr[str] 

@CustomResult[float, str]
def f(n: float):
    return 1 / n


v = f(10.0) # Ok[<class 'float'>]
r: float = v.unwrap_or(10.1) # 0.1
```

Using decorators to obtain Err.
Custom result type and custom Err type
```python
from thresult import Result, Ok, Err


class CustomOk(Ok):
    pass


class CustomErr(Err):
    pass


CustomResult: type = CustomOk[float] | CustomErr[str] 


@CustomResult[float, str]
def f(n: float):
    return 1 / n

v = f(0.0) # Err[<class 'str'>]
```

Using decorators to obtain Err.
Custom result type and custom Err type. 
Handling exceptions using *unwrap*
```python
from thresult import Result, Ok, Err


class CustomOk(Ok):
    pass


class CustomErr(Err):
    pass


CustomResult: type = CustomOk[float] | CustomErr[str] 


@CustomResult[float, str]
def f(n: float):
    return 1 / n


v = f(0.0) # Err[<class 'str'>]

try:
    v.unwrap()
except ZeroDivisionError as e:
    pass
```

Using decorators to obtain Err.
Custom result type and custom Err type.
Handling exceptions using *unwrap_value*
```python
from thresult import Result, Ok, Err


class CustomOk(Ok):
    pass


class CustomErr(Err):
    pass


CustomResult: type = CustomOk[float] | CustomErr[str] 


@CustomResult[float, str]
def f(n: float):
    return 1 / n


v = f(0.0) # Err[<class 'str'>]
message: str = v.unwrap_value() # float division by zero
```

Using decorators to obtain Err.
Custom result type and custom Err type.
Handling exceptions using *unwrap_or*
```python
from thresult import Result, Ok, Err


class CustomOk(Ok):
    pass


class CustomErr(Err):
    pass


CustomResult: type = CustomOk[float] | CustomErr[str] 


@CustomResult[float, str]
def f(n: float):
    return 1 / n


v = f(0.0) # Err[<class 'str'>]
message: str = v.unwrap_or('Custom message') # Custom message
```

Using *wrap_result* decorator.
*wrap_result* decorator can be used on non-asynchronous and asynchronous functions.
Those functions will return Ok or Err type.

Using *wrap_result* on non-asynchronous functions which returns Ok type.
```python
from thresult import Result, wrap_result

@wrap_result(Result[int, Exception])
def f(n: float):
    return 1.0 / n

r: Result = f(2.1) # Ok object

```

Using *unwrap*, *unwrap_value* and *unwrap_or* with *wrap_result* on 
non-asynchronous functions which returns Ok type.
```python
from thresult import Result, wrap_result

@wrap_result(Result[int, Exception])
def f(n: float):
    return 1.0 / n

# handling exceptions when using unwrap
v:float
try:
    v = (f(2.0)).unwrap() # v is 0.5
except ZeroDivisionError as e:
    v = 0.0 

s:str = (f(2.0)).unwrap_value() # s is 0.5

r:float = (f(2.0)).unwrap_or('custom error message') # r is 0.5

o:float = (f(2.0)).unwrap_or(0.0) # o is 0.5

```

Using *wrap_result* on non-asynchronous functions which returns Err type.
```python
from thresult import Result, wrap_result

@wrap_result(Result[int, Exception])
def f(n: float):
    return 1.0 / n

r: Result = f(0.0) # Err object

```

Using *unwrap*, *unwrap_value* and *unwrap_or* with *wrap_result* on 
non-asynchronous functions which returns Err type.
```python
from thresult import Result, wrap_result

@wrap_result(Result[int, Exception])
def f(n: float):
    return 1.0 / n

# handling exceptions when using unwrap
v:float
try:
    v = (f(0.0)).unwrap()
except ZeroDivisionError as e:
    v = 0.0 # v is 0.0

s:str = (f(0.0)).unwrap_value() # s is float division by zero

r:str = (f(0.0)).unwrap_or('custom error message') # r has value custom error message

o:float = (f(0.0)).unwrap_or(0.0) # o has value 0.0

```

Using *wrap_result* on asynchronous functions which returns Ok type.
```python
from thresult import Result, wrap_result

@wrap_result(Result[int, Exception])
async def f(n: float):
    return 1.0 / n

r: Result = await f(2.1) # Ok object

```

Using *unwrap*, *unwrap_value* and *unwrap_or* with *wrap_result* on 
asynchronous functions which returns Ok type.
```python
from thresult import Result, wrap_result

@wrap_result(Result[int, Exception])
async def f(n: float):
    return 1.0 / n

# handling exceptions when using unwrap
v:float
try:
    v = (await f(2.0)).unwrap() # v is 0.5
except ZeroDivisionError as e:
    v = 0.0 

s:str = (await f(2.0)).unwrap_value() # s is 0.5

r:float = (await f(2.0)).unwrap_or('custom error message') # r is 0.5

o:float = (await f(2.0)).unwrap_or(0.0) # o is 0.5

```

Using *wrap_result* on asynchronous functions which returns Err type.
```python
from thresult import Result, wrap_result

@wrap_result(Result[int, Exception])
async def f(n: float):
    return 1.0 / n

r: Result = await f(0.0) # Err object

```

Using *unwrap*, *unwrap_value* and *unwrap_or* with *wrap_result* on 
asynchronous functions which returns Err type.
```python
from thresult import Result, wrap_result

@wrap_result(Result[int, Exception])
async def f(n: float):
    return 1.0 / n

# handling exceptions when using unwrap
v:float
try:
    v = (await f(0.0)).unwrap()
except ZeroDivisionError as e:
    v = 0.0 # v is 0.0

s:str = (await f(0.0)).unwrap_value() # s is float division by zero

r:str = (await f(0.0)).unwrap_or('custom error message') # r has value custom error message

o:float = (await f(0.0)).unwrap_or(0.0) # o has value 0.0

```


<!-- Links -->

<!-- Badges -->
[bsd3-image]: https://img.shields.io/badge/License-BSD_3--Clause-blue.svg
[bsd3-url]: https://opensource.org/licenses/BSD-3-Clause
[build-image]: https://img.shields.io/badge/build-success-brightgreen
[coverage-image]: https://img.shields.io/badge/Coverage-100%25-green

[pypi-project-url]: https://pypi.org/project/thresult/
[stable-ver-image]: https://img.shields.io/pypi/v/thresult?label=stable
[python-ver-image]: https://img.shields.io/pypi/pyversions/thresult.svg?logo=python&logoColor=FBE072
[status-image]: https://img.shields.io/pypi/status/thresult.svg

