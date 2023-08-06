import setuptools

setuptools.setup(
    name="pyicacls",
    version="1.0.0",
    author="GefGef",
    author_email="gefen102@gmail.com",
    description="A package to show and set windows files permissions",
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