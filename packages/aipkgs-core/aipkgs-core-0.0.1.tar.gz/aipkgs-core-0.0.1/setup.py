import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aipkgs-core",
    version="0.0.1",
    author="Alexy",
    author_email="",
    description="AI's Packages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/aipy/common",
    project_urls={
        "Issues": "https://gitlab.com/aipy/common/-/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires='>=3.6',
)
