import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

requirements=["pygame>=2.0.0"]

setuptools.setup(
    name="SubFoldersProject",
    version="1.0.0",
    author="Andy931",
    author_email="andy@randy.ru",
    description="A small example Sub Folders package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.randy.ru",
    project_urls={
        "Docs": "https://docs.randy.ru",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    #package_dir={"": "SubFoldersProject"},
    packages=setuptools.find_packages(),
    python_requires=">=3.5",
    include_package_data=True,
    install_requires=requirements,
    
  
)