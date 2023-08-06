import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xyce",
    version="7.4.0",
    author="Xyce Team",
    author_email="xyce@sandia.gov",
    description="Xyce",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Xyce/Xyce",
    project_urls={
        "Bug Tracker": "https://github.com/Xyce/Xyce/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
