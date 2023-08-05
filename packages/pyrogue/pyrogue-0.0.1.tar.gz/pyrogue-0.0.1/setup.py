import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyrogue",
    version="0.0.1",
    author="Will Butler",
    author_email="will@aerenserve.net",
    description="An extensible nethack style roguelike",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/whilb/roguelike",
    project_urls={
        "Bug Tracker": "https://github.com/whilb/roguelike/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
)
