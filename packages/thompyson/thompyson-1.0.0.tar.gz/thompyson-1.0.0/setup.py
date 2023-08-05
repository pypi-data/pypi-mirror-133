import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="thompyson",
    version="1.0.0",
    author="William Angus",
    author_email="william@ngus.co.uk",
    description="Utility for computations in R J Thompson's groups F and T.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url = "https://github.com/WilliamAngus/thompyson",
    project_urls={
        "Bug Tracker" : "https://github.com/WilliamAngus/thompyson/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Operating System :: OS Independent",
    ],
    package_dir={"" : "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)

