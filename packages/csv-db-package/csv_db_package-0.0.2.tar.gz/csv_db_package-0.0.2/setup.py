import setuptools

with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

setuptools.setup(
    name="csv_db_package",
    version="0.0.2",
    author="Ankita Liya",
    author_email="ankitaliya321@gmail.com",
    description="This package is found useful for those who wants to modify their CSV file without using database."
                "It creates a local server that having a functionality of uploading a csv file and "
                "then perform crud operations through browser itself."
                ,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ankitaliya/csv_db_package",
    project_urls={
        "Bug Tracker": "https://github.com/ankitaliya/csv_db_package/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    package_data={'csv_db_package': ['Templates/*.html']},
    install_requires=['mysql-connector-python', 'Jinja2', 'pandas'],
    python_requires=">=3.7",
)