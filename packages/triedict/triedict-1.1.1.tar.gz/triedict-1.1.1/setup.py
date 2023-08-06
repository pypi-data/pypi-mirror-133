# -*- coding: UTF-8 -*-
"""vega FYI
    @author: vegaviazhang
    @file:setup.py
    @time:2021/10/04
"""
from setuptools import setup, find_packages

setup(
    name='triedict',
    version="1.1.1",
    description=(
        '基于字典树的匹配'
    ),
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    author='vegaviazhang',
    author_email='vegaviazhang@gmail.com',
    maintainer='vega',
    maintainer_email='vegaviazhang@gmail.com',
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/vegaviazhang/triedict',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[]
)
