from setuptools import setup
from setuptools import find_packages

setup(name='hsiehpinghan_setuptools_test',
      version='0.0.1',
      install_requires=['numpy'],
      packages=find_packages(where='src',
                             include=['my_package_0', 'my_package_2'],
                             exclude=['my_package_1']),
      package_dir={'': 'src'})