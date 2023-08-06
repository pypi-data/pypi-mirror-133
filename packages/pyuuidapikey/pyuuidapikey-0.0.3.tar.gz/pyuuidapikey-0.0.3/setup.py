import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyuuidapikey", # Replace with your own username
    version="0.0.3",
    author="Kumara Fernando",
    author_email="mklmfernando@gmail.com",
    description="A Simple package to generate and validate UUID and API key pairs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kumaF/py-uuid-apikey",
    packages=setuptools.find_packages(),
    install_requires=[            # I get to this in a second
          'BaseHash'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)