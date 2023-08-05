from distutils.core import setup
from setuptools import find_packages

with open("README.rst", "r") as f:
    long_description = f.read()

setup(
    name='pytensordb',
    version='1.0.0',
    description='TensorDB API(Python)',
    long_description=long_description,
    author='上海爱可生信息技术股份有限公司',
    author_email='zhoupeng@actionsky.com',
    install_requires=[],
    url='https://www.actionsky.com/Cloud-tree-series/tensordb.html',
    packages=find_packages(),
    include_package_data=True,
    license='Apache LICENSE 2.0',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries'
    ],
)
