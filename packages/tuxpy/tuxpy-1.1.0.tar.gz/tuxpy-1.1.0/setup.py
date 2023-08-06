import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tuxpy",
    version="1.1.0",
    author="burakpadr",
    author_email="b.padir99@gmail.com",
    description="This API was created to operate the TuxDB processes with Python Programming Language.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/burakpadr/tuxpy",
    project_urls={
        "Bug Tracker": "https://github.com/burakpadr/tuxpy/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["requests"],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
)
