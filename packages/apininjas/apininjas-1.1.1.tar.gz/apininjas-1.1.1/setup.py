import setuptools


setuptools.setup(
    name="apininjas",  # This is the name of the package
    version="1.1.1",  # The initial release version
    author="Jawad Abdulrazzaq",  # Full name of the author
    description="API Ninjas Python Wrapper",
    long_description="API Ninjas python wrapper",  # Long description read from the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),  # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],  # Information to filter the project on PyPi website
    python_requires='>=3.6',  # Minimum version requirement of the package
    py_modules=["apininjas"],  # Name of the python package
    package_dir={'': 'apininjas'},  # Directory of the source code of the package
    install_requires=['requests']  # Install other dependencies if any

)
