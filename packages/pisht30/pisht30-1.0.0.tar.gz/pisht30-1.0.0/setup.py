from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pisht30',
    version='1.0.0',
    author='Akihisa ONODA',
    author_email='akihisa.onoda@osarusystem.com',
    description='To use SHT30 with pigpio',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Langur/pisht30',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.7',
    ],
    package_dir={"": "src"},
    packages=['pisht30'],
    install_requires=['pigpio'],
    license='MIT',
    keywords='pisht30 sht30 sht31 sht35 env2hat env3hat pigpio temperature humidity sensor i2c',

)
