import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="orangesms",
    version="0.0.2",
    author="Honorable Con",
    author_email="honorablecon@gmail.com",
    description="This packages aims to let you quickly send SMS from Python using the Orange SMS API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/honorableCon/OrangeSMS-API",
    project_urls={
        "Bug Tracker": "https://github.com/honorableCon/OrangeSMS-API/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "package"},
    packages=setuptools.find_packages(where="package"),
    python_requires=">=3.6",
)