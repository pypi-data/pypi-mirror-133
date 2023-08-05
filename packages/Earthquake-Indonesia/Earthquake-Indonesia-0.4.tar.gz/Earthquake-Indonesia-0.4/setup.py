"""
https://packaging.python.org/en/latest/tutorials/packaging-projects/
"""
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Earthquake-Indonesia",
    version="0.4",
    author="Ahmad Fauzan Z",
    author_email="ahmadfauzanzain10@gmail.com",
    description="This Package will get the latest eartquake from BMKG |Meteorogical, Climatological, and Geophysical agency",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ahmadfauzan1922/Earthquake-Indonesia",
    # project_urls={
    #     "Bug Tracker": " https://remoteworker.id",
    # },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable"
    ],
    # package_dir={"": "src"},
    # packages=setuptools.find_packages(where="src"),
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
