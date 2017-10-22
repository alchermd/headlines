from setuptools import setup

setup(
    name="headlines",
    version="0.1",
    packages=["headlines"],
    install_requires=[
        "flask", 
        "requests"
    ],
    include_package_data=True,
)