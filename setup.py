# coding: utf-8
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wechat_msg",
    version="0.2",
    author="wnma3mz",
    author_email="",
    description="wechat send message",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wnma3mz/wechat_msg",
    packages=setuptools.find_packages(),
    install_requires=['requests>=2.20.0'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)