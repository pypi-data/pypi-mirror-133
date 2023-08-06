# coding=utf-8
# !/usr/bin/env python
# @Author: zhaoyi
# @Time: 2022-01-07 14:44
import setuptools

setuptools.setup(

    name="pytest-testpluggy",  # Replace with your own username

    version="0.0.1",

    author="zhaoyi",

    author_email="2284401112@qq.com",

    description="set your encoding",

    long_description="show Chinese for your mark.parametrize().",

    classifiers=["Programming Language :: Python :: 3", "Framework :: Pytest", ],

    packages=['test_pluggy'],

    keywords=["pytest", "py.test", "pytest_pluggy", ],

    install_requires=['pytest'],

    python_requires=">=3.6",

    # 入口模块或者入口函数

    entry_points={'pytest11': ['pytest-testpluggy = test_pluggy']},

    zip_safe=False,

)
