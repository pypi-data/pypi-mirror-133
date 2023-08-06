from setuptools import setup, find_packages

VERSION = '0.11'
DESCRIPTION = 'My first Python package1'
LONG_DESCRIPTION = 'My first Python package1 with a slightly longer description'

# Setting up
setup(
    # the name must match the folder name 'verysimple23'
    name="verysimple23",
    version=VERSION,
    author="Pooja Singla",
    author_email="pooja_singla@persistent.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['python', 'first package'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)