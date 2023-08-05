import setuptools

with open("README.md", "r", encoding="utf-8") as desc_file:
    long_description = desc_file.read()

setuptools.setup(
    name="pylinqlib",
    version="1.0.4",
    author="crimsondevel",
    author_email="crimsondevel@gmail.com",
    description="LINQ implementation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={".": "src"},
    packages=setuptools.find_packages(where="pylinqlib"),
    python_requires=">=3.8",
)
