import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="openapi-schema-generator",
    version="1.0.1",
    author="Elyashiv Danino",
    author_email="elyashiv3839@gmail.com",
    description="Resolve schema and deploy to single schema",
    long_description="file: README.md",
    long_description_content_type="text/markdown",
    url="https://github.com/elyashiv3839/openapi-schema-generator.git",
    download_url="https://github.com/elyashiv3839/openapi-schema-generator/archive/refs/tags/1.0.1.tar.gz",
    project_urls={"Bug Tracker": "https://github.com/elyashiv3839/openapi-schema-generator.git/issues"},
    classifier=[
        "Programming Language :: Python :: 3",
        "Licence :: MIT",
        "Operating System :: Multi-platform",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=["attrs==21.2.0", "importlib-metadata==4.8.1", "isodate==0.6.0", "jsonschema==3.2.0",
                      "openapi-schema-validator==0.1.5", "pyrsistent==0.18.0", "PyYAML==5.4.1", "six==1.16.0",
                      "typing-extensions==3.10.0.2", "zipp==3.5.0",
                      "compare_objects==1.0.0"]
)
