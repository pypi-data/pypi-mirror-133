from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.16'
DESCRIPTION = ' i2c 16*2 lcd library for esp32 divkit v1'
LONG_DESCRIPTION = 'A package that allows to manage and control i2c lcd in a simple way.'

# Setting up
setup(
    name="i2c_lcd_esp32",
    version=VERSION,
    author="sami.moona",
    author_email="<saminsx@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['i2c', 'lcd', '16*2', 'esp32', 'divkit', 'wroom-32'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",

        "Programming Language :: Python :: Implementation :: MicroPython"
    ]
)
