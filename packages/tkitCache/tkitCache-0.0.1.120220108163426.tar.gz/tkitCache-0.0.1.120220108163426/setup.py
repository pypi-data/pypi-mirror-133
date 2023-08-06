# -*- coding: utf-8 -*-
"""
作者：　terrychan
Blog: https://terrychan.org
# 说明：

"""
import os
# -*- coding: utf-8 -*-
from setuptools import find_packages, setup
from os import path as os_path
import time
this_directory = os_path.abspath(os_path.dirname(__file__))

# 读取文件内容
def read_file(filename):
    with open(os_path.join(this_directory, filename), encoding='utf-8') as f:
        long_description = f.read()
    return long_description

# 获取依赖
def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]
long_description="""

这里是说明

cache操作。


https://github.com/napoler/tkitCache/

"""
setup(
    name='tkitCache',
    version='0.0.1.1'+time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())),
    description='Terry toolkit tkitCache',
    author='Terry Chan',
    author_email='napoler2008@gmail.com',
    url='https://github.com/napoler/tkitCache/',
    # install_requires=read_requirements('requirements.txt'),  # 指定需要安装的依赖
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'cacheout==0.13.1',

    ],
    packages=['tkitCache'])

"""
pip freeze > requirements.txt

python3 setup.py sdist
#python3 setup.py install
python3 setup.py sdist upload
"""
if __name__ == '__main__':
    pass
