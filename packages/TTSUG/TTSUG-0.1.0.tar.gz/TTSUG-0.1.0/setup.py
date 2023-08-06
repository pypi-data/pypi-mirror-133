from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "readme.md").read_text()

setup(
    name='TTSUG',
    version='0.1.0',
    description='A Python package for converting the text to speech',
    long_description=long_description,
    long_description_content_type = 'text/markdown',
    url='https://github.com/swadeshrd/tts',
    author='Swadesh Ranjan Dash',
    author_email='swadesh5dash@gmail.com',
    license='MIT',
    packages=['tts'],
    install_requires=['requests'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)