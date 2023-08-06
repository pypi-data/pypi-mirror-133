# ！usr/bin/env python
# -*- coding: utf-8 -*-
# Time : 2021/12/15 19:52
# @Author : LucXiong
# @Project : Model
# @File : setup.py
# https://blog.csdn.net/weixin_49246443/article/details/108425035
from setuptools import setup, find_packages

setup(
    name="swarm_algorithm",
    version="0.0.3",
    author="Luc",
    author_email="xionglei@sjtu.edu.cn",
    description="",
    long_description_content_type="text/markdown",
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    install_requires=[],  # install_requires字段可以列出依赖的包信息，用户使用pip或easy_install安装时会自动下载依赖的包
    url='https://github.com',
    license='MIT',
    packages=find_packages(),  # 需要处理哪里packages，当然也可以手动填，例如['pip_setup', 'pip_setup.ext']
    include_package_data=False,
    zip_safe=True,
)