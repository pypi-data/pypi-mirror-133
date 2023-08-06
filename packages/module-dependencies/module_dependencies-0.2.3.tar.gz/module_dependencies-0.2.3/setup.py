from setuptools import find_packages, setup

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="module_dependencies",
    version="0.2.3",
    url="https://github.com/tomaarsen/module_dependencies",
    project_urls={
        "Documentation": "https://tomaarsen.github.io/module_dependencies/",
        "Source Code": "https://github.com/tomaarsen/module_dependencies",
        "Issue Tracker": "https://github.com/tomaarsen/module_dependencies/issues",
    },
    license="MIT",
    author="Tom Aarsen",
    author_email="ta.aarsen@gmail.com",
    description="Gather module dependencies of source code",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
    install_requires=required,
    zip_safe=False,
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    include_package_data=True,
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
