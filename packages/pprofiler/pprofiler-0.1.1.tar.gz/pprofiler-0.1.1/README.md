# pprofiler

Simple Python Decorator to Profiling Function or Method

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install pprof.

```bash
pip install pprof
```

## Usage

```python
# profiling.py

from pprofiler import pprof

@pprof()
def method_to_profile():
    # do some task
    print("value")

method_to_profile()
```

it will resulting cProfile output on console

```bash
$ python ./profiling.py
value
         3 function calls in 0.000 seconds

   Ordered by: call count

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.000    0.000 {built-in method builtins.print}
        1    0.000    0.000    0.000    0.000 <ipython-input-8-fb2a62e7b3fa>:1(test)
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
