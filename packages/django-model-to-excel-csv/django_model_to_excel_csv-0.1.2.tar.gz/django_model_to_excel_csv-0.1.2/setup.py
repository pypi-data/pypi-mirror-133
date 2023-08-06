import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django_model_to_excel_csv",
    version="0.1.2",
    author="H I Govinda",
    author_email="higovind5@email.com",
    description="Simple Excel and CSV file Generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/pypa/sampleproject",
    # project_urls={
    #     "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    # },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)