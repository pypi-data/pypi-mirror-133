from setuptools import setup

with open('README.md','r') as fh:
    long_desc = fh.read()
setup(
    name='decision-tree-ID3-Algorithm',
    version='0.0.2',
    description='Desicion Tree Algorithms',
    py_modules=['buildTree','classify_data','ID3Algorithm','node'],
    package_dir={'':'src'},
    classifiers=["Intended Audience :: Education", 
    "Operating System :: OS Independent", 
    "Programming Language :: Python :: 3.0",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8"],
    long_description=long_desc,
    long_description_content_type="text/markdown",
    install_requires=['treelib']
)