# -*- coding: utf-8 -*-

import os
from distutils.core import setup
from pathlib import Path


this_directory = Path(__file__).parent
long_description = (this_directory / 'README.md').read_text()


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


extra_files = package_files('pyAudioAnalyzer')
setup(
    name='pyAudioAnalyzer',
    version='0.2.2',
    description='Python library for vibrational analysis of audio',
    author='E. J. Wehrle',
    url='https://github.com/e-dub/pyAudioAnalyzer',
    package_data={'': extra_files},
    license='gpl-3.0',
    packages=['pyAudioAnalyzer'],
    install_requires=[
        'scipy',
        'numpy',
        'matplotlib',
        'seaborn',
        'playsound',
        'pyfftw',
        'librosa',
        'gtts',
        'sounddevice',
        'pydub',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
)
