from setuptools import setup, find_packages

setup(
    name="sentinelcodeai",
    version="1.0",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "sentinel=src.cli.main:main",
        ],
    },
)