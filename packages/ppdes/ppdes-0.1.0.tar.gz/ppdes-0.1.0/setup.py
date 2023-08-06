from setuptools import *

setup(
    name="ppdes",
    version="0.1.0",
    keywords=("math",),
    description="a ped solver",
    long_description="a ped solver",
    license="MIT Licence",

    packages=find_packages(),
    include_package_data=True,
    platforms=["all"],
    python_requires='>=3',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
