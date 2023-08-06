from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.13'
DESCRIPTION = 'Streaming video data via networks'
LONG_DESCRIPTION = 'A package that allows to build simple streams of video, audio and camera data.'
setup(
    name="mangekyo",
    version="0.0.1",
    author="Isao Toyama",
    author_email="isaotv@gmail.com",
    description="Kaleidoscope package",
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/isaotoyama/kaleidoscope",
    project_urls={
        "Bug Tracker": "https://github.com/isaotoyama/kaleidoscope/issues",
    },    keywords=['ComputerVision', 'HandTracking', 'FaceTracking', 'PoseEstimation'],
    install_requires=[
        'opencv-python',
        'numpy'
    ],
    classifiers=[
         'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',  # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ]
)


