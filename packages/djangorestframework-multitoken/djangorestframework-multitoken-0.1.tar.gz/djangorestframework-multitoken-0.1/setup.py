import pathlib
from setuptools import setup

README = (pathlib.Path(__file__).parent / "README.md").read_text()

setup(
    name="djangorestframework-multitoken",
    version="0.1",
    description="Version of Django REST Framework auth Token allowing multiple Tokens per User.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/nextlink/djangorestframework-multitoken",
    author="NextLink Labs",
    license="MIT",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    packages=["rest_framework_multitoken", "rest_framework_multitoken.management.commands", "rest_framework_multitoken.migrations"],
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=["djangorestframework>=3.12"],
)
