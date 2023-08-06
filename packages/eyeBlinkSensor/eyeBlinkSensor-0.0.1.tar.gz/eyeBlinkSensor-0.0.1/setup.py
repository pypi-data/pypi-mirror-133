from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.0.1'
DESCRIPTION = 'eye Blinker package'
LONG_DESCRIPTION = 'Whenever you blink your eye the eyeBlink Sensor module  will count it and show it on your screen. Addition to it, it specifies the graph of blibking of your eye'

# Setting up
setup(
    name="eyeBlinkSensor",
    version=VERSION,
    author="Rischit Aggarwal",
    author_email="<rischitcode365@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    long_description= LONG_DESCRIPTION,
    install_requires=[],
    keywords=['opencv', 'FaceMesh', 'mediapipe' ,'LivePlot'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)