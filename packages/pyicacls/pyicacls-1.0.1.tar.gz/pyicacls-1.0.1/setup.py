import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyicacls",
    version="1.0.1",
    author="GefGef",
    author_email="gefen102@gmail.com",
    description="A package to show and set windows files permissions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["pyicacls"],
    install_requires=[
        'impacket~=0.9.23'
    ],
)