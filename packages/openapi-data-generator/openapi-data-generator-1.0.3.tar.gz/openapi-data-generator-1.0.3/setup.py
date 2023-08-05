import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="openapi-data-generator",
    version="1.0.3",
    author="elyashiv3839, RAZALKALY",
    author_email="elyashiv3839@gmail.com, RAZALKALY@YAHOO.COM",
    description="Generate all valid and invalid permutations of payloads - according OpenAPI specification",
    long_description="file: README.md",
    long_description_content_type="text/markdown",
    url="https://github.com/elyashiv3839/openapi-data-generator.git",
    download_url="https://github.com/elyashiv3839/openapi-data-generator/archive/refs/tags/1.0.3.tar.gz",
    project_urls={"Bug Tracker": "https://github.com/elyashiv3839/openapi-data-generator.git/issues"},
    classifier=[
        "Programming Language :: Python :: 3",
        "Licence :: MIT",
        "Operating System :: Multi-platform",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=["openapi-schema-generator==1.0.1", "rstr==3.0.0", "filelock==3.4.2"]
)
