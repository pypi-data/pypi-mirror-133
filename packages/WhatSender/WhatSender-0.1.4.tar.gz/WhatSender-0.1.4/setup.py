from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.1.4'
DESCRIPTION = 'Sending Whatsapp messages.'
LONG_DESCRIPTION = 'A package that allows to send Whatsapp messages, by given number, message, and time.'

# Setting up
setup(
    name="WhatSender",
    version=VERSION,
    author="GodZilo (Ido Barel)",
    author_email="<vikbarel5@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pyautogui', 'termcolor', 'pyperclip'],
    keywords=['python', 'Whatsapp', 'message', 'Whatsapp sender', 'message sender'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)