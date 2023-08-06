import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="converter-priyanka",
    version="0.1.1",
    author="Priyanka Sirohiya",
    author_email="priyanka.sirohiya@gmail.com",
    description="A package for generating API data reports in different formats",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/priyankacode-123/Training",
    project_urls={
        "Bug Tracker": "https://github.com/priyankacode-123/Training",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "APIcall"},
    packages=setuptools.find_packages(where="APIcall"),
    install_requires=['pandas', 'requests', 'pdfkit', 'lxml', 'openpyxl'],
    python_requires=">=3.6",
)