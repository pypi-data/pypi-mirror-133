from setuptools import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='Pytools-kit',
    version='0.0.1',
    description='PyTool-Kit is an Python tools. It contain many usefull Tools',
    author= 'Prajwal Kedari',
    url = 'https://github.com/prajwalkedari/PyTool-Kit',
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    keywords=['Python','Tool','kit','Toolkit','Pytool-Kit','prajwalkedari' , 'Prajwal','kedari'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.x',
    py_modules=['PyTool_Kit'],
    package_dir={'':'src'},
    install_requires = ['']
)
