import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tencent-cos-python-azleal",
    version="0.0.5",
    author="Azleal",
    author_email="azleal.mr@gmail.com",
    description="easy use for tencent_cos_python client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Azleal/tencent-cos-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "cos-python-sdk-v5"
    ]
)