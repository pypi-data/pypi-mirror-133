from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'A simple ML model to classify Spotify tracks using audio features.'
LONG_DESCRIPTION = 'A simple ML model to classify Spotify tracks using audio features.'

setup(
    name="spotifymoods",
    version=VERSION,
    author="Ammar Oker",
    author_email="<oker.ammar@gmail.com>",
    url="https://github.com/ammar-oker/spotifymoods",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pandas', 'scikit_learn'],
    keywords=['spotify', 'machine learning', 'spotify moods', 'spotify emotions'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
    ]
)
