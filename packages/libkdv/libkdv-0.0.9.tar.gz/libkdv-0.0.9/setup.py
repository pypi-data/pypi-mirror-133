#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: Kerple GL Plugin
# Mail: www.1nick@gmail.com
# Created Time:  2021-12-22 19:17:34
#############################################

from setuptools import setup, find_packages   

setup(
    name = "libkdv",
    version = "0.0.9",
    keywords = ["pip", "KDE","heatmap","KDV","KeplerGL"],
    description = "KDV",
    long_description = "A library of feature heatmap algorithm",
    license = "MIT Licence",

    url = "https://github.com/libkdv",  
    author = "Kerple GL Plugin",
    author_email = "www.1nick@gmail.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["numpy","pandas","keplergl",""]        
)