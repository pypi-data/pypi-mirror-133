'''
Author: F.w 164175317@qq.com
Date: 2021-12-01 10:39:50
LastEditors: F.w 164175317@qq.com
LastEditTime: 2022-01-07 16:42:07
'''
from setuptools import setup, find_packages

setup(
    name = 'XBoss',
    version = '0.0.2',
    keywords='XBOSS',
    description = 'a library for xb_boss Developer',
    license = 'MIT License',
    url = 'https://github.com/feignwf',
    author = 'F.w',
    author_email = '164175317@qq.com',
    packages = find_packages(),
    include_package_data = True,
    platforms = 'any',
    install_requires = [
        'requests>=2.25.1',
        'pandas>=1.2.4'
        ],
)