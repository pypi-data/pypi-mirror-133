from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize
import Cython.Compiler.Options
Cython.Compiler.Options.annotate = True
import pysam


"""
python setup.py build_ext --inplace --force
"""

# setup(ext_modules=cythonize(
#     Extension(
#         'basecount',
#         sources=['basecount.pyx'],
#         language='c',
#         include_dirs=pysam.get_include(),
#         define_macros=pysam.get_defines(),
#         extra_compile_args=['-fopenmp'],
#         extra_link_args=['-fopenmp'],
#         annotate=True,
#     )
# ))





# require pysam is pre-installed
try:
    import pysam
except ImportError:
    raise Exception('pysam not found; please install pysam first')
from distutils.version import LooseVersion
required_pysam_version = '0.18.0'
if LooseVersion(pysam.__version__) < LooseVersion(required_pysam_version):
    raise Exception('pysam version >= %s is required; found %s' %
                    (required_pysam_version, pysam.__version__))


def get_version():
    """Extract version number from source file."""
    from ast import literal_eval
    with open('bamstats/__init__.py') as f:
        for line in f:
            if line.startswith('__version__'):
                return literal_eval(line.partition('=')[2].lstrip())
    raise ValueError("__version__ not found")



print('[bamstats] build with Cython')
extensions = cythonize(
    Extension('bamstats.opt',
                sources=['bamstats/opt.pyx'],
                language = 'c',
                include_dirs=pysam.get_include(),
                define_macros=pysam.get_defines(),
                annotate=True,)
)



setup(
    name='bamstats',
    version=get_version(),
    author='Lianlin',
    author_email='LianLin@hectobio.com',
    url='',
    license='',
    description='A Python utility for calculating statistics against nCov-2019 genome '
                'position based on sequence alignments from a '
                'BAMfile.',
    scripts=['scripts/bamstats'],
    package_dir={'': '.'},
    install_requires=[
        "pysam (>=0.18)",
    ],
    packages=find_packages(),
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    ext_modules=extensions,
)
