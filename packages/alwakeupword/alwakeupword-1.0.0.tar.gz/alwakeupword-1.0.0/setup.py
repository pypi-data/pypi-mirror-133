from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

def requirements():
    with open('requirements.txt') as f:
        REQUIREMENTS = [req.replace('\n','') for req in f.readlines()]
    return REQUIREMENTS

setup(
    name="alwakeupword",
    version="1.0.0",
    description="alwakeupword explicitly request the attention of a computer using a wake up word and also allows user to make dataset and train a model of their own wake up word.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/alankarartist/alwakeupword",
    author="Alankar Singh",
    author_email="alankarartist@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements(),
    entry_points={
        "console_scripts": [
            "alwakeupword=alwakeupword.cli:main",
        ]
    }
)