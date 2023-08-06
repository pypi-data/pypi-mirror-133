# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['pprofiler']
setup_kwargs = {
    'name': 'pprofiler',
    'version': '0.1.0',
    'description': 'Python Decorator for Profiling Function or Method',
    'long_description': '# pprofiler\n\nSimple Python Decorator to Profiling Function or Method\n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install pprof.\n\n```bash\npip install pprof\n```\n\n## Usage\n\n```python\n# profiling.py\n\nfrom pprof import pprof\n\n@pprof()\ndef method_to_profile():\n    # do some task\n    print("value")\n\nmethod_to_profile()\n```\n\nit will resulting cProfile output on console\n\n```bash\n$ python ./profiling.py\nvalue\n         3 function calls in 0.000 seconds\n\n   Ordered by: call count\n\n   ncalls  tottime  percall  cumtime  percall filename:lineno(function)\n        1    0.000    0.000    0.000    0.000 {built-in method builtins.print}\n        1    0.000    0.000    0.000    0.000 <ipython-input-8-fb2a62e7b3fa>:1(test)\n        1    0.000    0.000    0.000    0.000 {method \'disable\' of \'_lsprof.Profiler\' objects}\n```\n\n## License\n[MIT](https://choosealicense.com/licenses/mit/)\n',
    'author': 'Ngalim Siregar',
    'author_email': 'ngalim.siregar@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nsiregar/pprof',
    'package_dir': package_dir,
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
