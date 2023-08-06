from distutils.core import setup
from Cython.Build import cythonize
    
setup(
    name = 'calculator_lzh',
    # ext_modules = cythonize("calculator.py"),
    packages=["calculator"],
    python_requires=">=3",
    version="2.0.0",
    entry_points={
        'console_scripts': ['calculator:calculator:run','ctor:calculator:run']
    },
)