import os
import re
from setuptools import find_packages, setup

# READ README MD FOR long_description
with open('README.md', 'rb') as f:
    readme = f.read().decode('utf-8')

package = 'friendly_arguments'
with open(os.path.join(package, '__init__.py'), 'rb') as f:
    init_py = f.read().decode('utf-8')

version = re.search('^__version__ = [\'\"]([^\'\"]+)[\'\"]', init_py, re.MULTILINE).group(1)
author = re.search('^__author__ = [\'\"]([^\'\"]+)[\'\"]', init_py, re.MULTILINE).group(1)
email = re.search('^__email__ = [\'\"]([^\'\"]+)[\'\"]', init_py, re.MULTILINE).group(1)
url = re.search('^__github__ = [\'\"]([^\'\"]+)[\'\"]', init_py, re.MULTILINE).group(1)

setup(
    name='friendly-arguments',
    packages=find_packages(),
    version=version,
    description='Easy way to use named arguments by means of python dictionaries',
    long_description=readme,
    long_description_content_type="text/markdown",
    author=author,
    author_email=email,
    url=url,
    install_requires=[],
    license='MIT',
    keywords=['dev', 'scripts', 'args', 'tools'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
)