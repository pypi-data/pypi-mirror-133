from setuptools import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='KeyGen_Python',
    version='0.0.1',
    description='PyKey-Gen Is Key Generator , That Expired Within Minute',
    author= 'Prajwal Kedari',
    url = 'https://github.com/prajwalkedari/PyKey-Gen',
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    keywords=['pythonkey_gen','pykey_gen','PyKey-Gen','Key','Gen','Secure','Generator', 'key Generator','key generate','prajwalkedari' , 'Prajwal','kedari'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.x',
    py_modules=['pykey_gen'],
    package_dir={'':'src'},
    install_requires = ['']
)
