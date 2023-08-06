from setuptools import setup

"""
:authors: Vladislav117
:license: Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2021 Vladislav117
"""

name = "gmlib"

version = "0.0.2"

author = "Vladislav117"
author_email = "siuetkysta@gmail.com"

description = ""

with open("README.md", encoding="utf-8") as fp:
    long_description = fp.read()

url = "https://github.com/Vladislav117/gmlib"
download_url = f"https://github.com/Vladislav117/vorld/archive/v{version}.zip"

package_license = "Apache License, Version 2.0 see LICENSE file"

packages = ["gmlib"]

install_requires = []

setup(
    name=name,
    version=version,

    author=author,
    author_email=author_email,

    description=description,
    long_description=long_description,

    url=url,
    download_url=download_url,

    license=package_license,

    packages=packages,
    install_requires=install_requires,
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
    ]
)
