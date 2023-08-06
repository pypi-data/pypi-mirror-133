import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="testOrganizer",
    version="0.0.7",
    author="smirad91",
    author_email="smirad91@gmail.com",
    description="Organize tests and show results",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/smirad91/testOrganize",
    project_urls={
        "Bug Tracker": "https://github.com/smirad91/testOrganize/issues",
    },
    install_requires=["tabulate"],
    keywords=["test", "before", "after", "automation", "result", "console", "output"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    packages=setuptools.find_packages()
)