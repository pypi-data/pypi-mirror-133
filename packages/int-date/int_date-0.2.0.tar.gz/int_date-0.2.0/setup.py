from setuptools import setup
import io
import os
import re

__author__ = 'Cedric Zhuang'


def version():
    desc = get_long_description()
    ret = re.findall(r'VERSION: (.*)', desc)[0]
    return ret.strip()


def here(filename=None):
    ret = os.path.abspath(os.path.dirname(__file__))
    if filename is not None:
        ret = os.path.join(ret, filename)
    return ret


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n\n')
    buf = []
    for filename in filenames:
        with io.open(here(filename), encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


def read_requirements(filename):
    with open(filename) as f:
        return f.read().splitlines()


def get_long_description():
    filename = 'README.md'
    return read(filename)


setup(
    name="int_date",
    version=version(),
    author="Cedric Zhuang",
    author_email="cedric.zhuang@gmail.com",
    description="Utility for int date like 20150312.",
    license="BSD",
    keywords="date integer",
    url="https://github.com/jealous/int_date",
    py_modules=['int_date'],
    platforms=['any'],
    long_description=get_long_description(),
    classifiers=[
        "Programming Language :: Python",
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    install_requires=read_requirements('requirements.txt'),
    tests_require=read_requirements('test-requirements.txt'),
    long_description_content_type='text/markdown',
)
