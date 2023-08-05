#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import warnings
from os.path import join, dirname
from setuptools import setup
from setuptools.extension import Extension
from setuptools.dist import Distribution

try:
    from cpuinfo import get_cpu_info
    CPU_FLAGS = get_cpu_info()['flags']
except Exception as exc:
    CPU_FLAGS = {}

try:
    from Cython.Distutils import build_ext
    USE_CYTHON = True
except ImportError:
    USE_CYTHON = False


class BinaryDistribution(Distribution):
    """
    Subclass the setuptools Distribution to flip the purity flag to false.
    See https://lucumr.pocoo.org/2014/1/27/python-on-wheels/
    """
    def is_pure(self):
        """Returns purity flag"""
        return False


CXXFLAGS = []

if os.name == "nt":
    CXXFLAGS.extend(["/O3"])
else:
    CXXFLAGS.extend([
        "-O3",
        "-Wno-unused-value",
        "-Wno-unused-function",
    ])


# Note: Only -msse4.2 has significant effect on performance;
# so not using other flags such as -maes and -mavx
if 'sse4_2' in CPU_FLAGS:
    warnings.warn("Compiling with SSE4.2 enabled")
    CXXFLAGS.append('-msse4.2')
else:
    warnings.warn("compiling without SSE4.2 support")


INCLUDE_DIRS = ['include']
CITY_HEADERS = [
    "include/citycrc.h",
    "include/city.h",
    "include/config.h",
]
FARM_HEADERS = [
    "include/farm.h",
]

CMDCLASS = {}
EXT_MODULES = []

if USE_CYTHON:
    CMDCLASS['build_ext'] = build_ext
    EXT_MODULES.extend([
        Extension(
            "cityhash",
            ["src/city.cc", "src/cityhash.pyx"],
            depends=CITY_HEADERS,
            language="c++",
            extra_compile_args=CXXFLAGS,
            include_dirs=INCLUDE_DIRS,
        ),
        Extension(
            "farmhash",
            ["src/farm.cc", "src/farmhash.pyx"],
            depends=FARM_HEADERS,
            language="c++",
            extra_compile_args=CXXFLAGS,
            include_dirs=INCLUDE_DIRS,
        )
    ])
else:
    EXT_MODULES.extend([
        Extension(
            "cityhash",
            ["src/city.cc", "src/cityhash.pyx"],
            depends=CITY_HEADERS,
            language="c++",
            extra_compile_args=CXXFLAGS,
            include_dirs=INCLUDE_DIRS,
        ),
        Extension(
            "farmhash",
            ["src/farm.cc", "src/farmhash.pyx"],
            depends=FARM_HEADERS,
            language="c++",
            extra_compile_args=CXXFLAGS,
            include_dirs=INCLUDE_DIRS,
        )
    ])


VERSION = '0.3.0.post2'
URL = "https://github.com/escherba/python-cityhash"


LONG_DESCRIPTION = """

"""


def get_long_description():
    fname = join(dirname(__file__), 'README.rst')
    try:
        with open(fname, 'rb') as fh:
            return fh.read().decode('utf-8')
    except Exception:
        return LONG_DESCRIPTION


setup(
    version=VERSION,
    description="Python bindings for CityHash and FarmHash",
    author="Alexander [Amper] Marshalov",
    author_email="alone.amper+cityhash@gmail.com",
    maintainer="Eugene Scherba",
    maintainer_email="escherba+cityhash@gmail.com",
    url=URL,
    download_url=URL + "/tarball/master/" + VERSION,
    name='cityhash',
    license='MIT',
    zip_safe=False,
    cmdclass=CMDCLASS,
    ext_modules=EXT_MODULES,
    keywords=['google', 'hash', 'hashing', 'cityhash', 'farmhash', 'murmurhash'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: C++',
        'Programming Language :: Cython',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities'
    ],
    long_description=get_long_description(),
    long_description_content_type='text/x-rst',
    tests_require=['pytest'],
    distclass=BinaryDistribution,
)
