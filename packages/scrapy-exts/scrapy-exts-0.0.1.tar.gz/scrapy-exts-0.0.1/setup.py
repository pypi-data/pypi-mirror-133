try:
    from setuptools import setup
except:
    from distutils.core import setup
import setuptools

setup(
    name='scrapy-exts',
    author='dragons',
    version='0.0.1',
    description='Scrapy辅助工具',
    long_description='Scrapy辅助工具, 拓展常用组件',
    author_email='521274311@qq.com',
    url='https://gitee.com/kingons/scrapy_tools',
    packages=setuptools.find_packages(),
    install_requires=[
        'scrapy>=2.2.0'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries',
    ],
    zip_safe=True,
)
