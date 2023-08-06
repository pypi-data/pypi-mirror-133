from distutils.core import setup
from Cython.Build import cythonize
    
setup(
    name = 'calculator_lzh',
    ext_modules = cythonize("calculator.py"),
    version="1.0.0",
)