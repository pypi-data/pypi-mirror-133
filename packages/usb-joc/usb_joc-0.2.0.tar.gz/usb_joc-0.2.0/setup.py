from os import read
from setuptools import setup

with open("README.md", "r", encoding="utf-8") as rm:
    readme = rm.read()

setup(
    name='usb_joc',
    version='0.2.0',    
    description='Send and receive JSON over USB CDC',
    long_description_content_type='text/markdown',
    long_description=readme,
    url='https://git.therode.net/jrode/jac',
    author='Jay Rode',
    author_email='jay@rode.dev',
    license='Mozilla Public License 2.0',
    packages=['joc'],
    install_requires=['pyserial',
                      'adafruit_board_toolkit',
                      'setuptools',
                      ],

    classifiers=[
        'Programming Language :: Python :: 3.9',
    ],
)
