from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = ''.join(["\n",fh.read()])

VERSION = '0.0.3'
DESCRIPTION = 'A package for getting python code from jupyter notebook.'

# Setting up
setup(
    name="ipynb_conversor",
    version=VERSION,
    author="Vitia Fritelle (Vitor Guilherme Coutinho de Barros Junior)",
    author_email="<vitorjunior448@gmail.com>",
    description=DESCRIPTION,
    license='MIT',
    long_description_content_type="text/markdown",
    long_description=long_description,
    url='https://github.com/vitia-fritelle/ipynb_converter',
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=['typing'],
    keywords=['python', 'jupyter notebook', 'converter'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        'Framework :: Jupyter',
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)