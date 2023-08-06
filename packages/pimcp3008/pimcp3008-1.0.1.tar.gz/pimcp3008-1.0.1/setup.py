from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pimcp3008',
    version='1.0.1',
    author='Akihisa ONODA',
    author_email='akihisa.onoda@osarusystem.com',
    description='To use MCP3008 with pigpio.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Langur/pimcp3008',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.7',
    ],
    package_dir={"": "src"},
    packages=['pimcp3008'],
    install_requires=['pigpio'],
    license='MIT',
    keywords='pimcp3008 mcp3004 mcp3008 pigpio adc analog-to-digital spi',

)
