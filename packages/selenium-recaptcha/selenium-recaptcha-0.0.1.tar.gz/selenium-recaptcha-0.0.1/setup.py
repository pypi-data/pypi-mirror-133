from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'reCaptcha v2 solver for selenium'
LONG_DESCRIPTION = 'A package that allows to solve reCaptcha v2 with selenium'

# Setting up
setup(
    name="selenium-recaptcha",
    version=VERSION,
    author="S M Shahriar Zarir",
    author_email="<shahriarzariradvance@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['SpeechRecognition', 'undetected-chromedriver', 'selenium'],
    keywords=['python', 'reCaptcha', 'stream', 'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)