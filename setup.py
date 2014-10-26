#!/usr/bin/env python

from setuptools import setup, find_packages

from greenrpc import __version__

with open("./requirements.txt") as fp:
    requirements = fp.read()
    requirements = requirements.split("\n")

setup(
    name="greenrpc",
    version=__version__,
    description="TCP & HTTP RPC Servers written with msgpack and gevent",
    author="Brett Langdon",
    author_email="brett@blangdon.com",
    url="https://github.com/brettlangdon/greenrpc",
    packages=find_packages(),
    license="MIT",
    scripts=["bin/greenrpc-server", "bin/greenrpc-client"],
    install_requires=requirements,
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Topic :: Utilities",
    ]
)
