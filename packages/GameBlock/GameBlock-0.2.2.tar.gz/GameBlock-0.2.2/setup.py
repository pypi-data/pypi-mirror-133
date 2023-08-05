import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="GameBlock",
    version="0.2.2",
    author="ApplesAndBananas",
    author_email="gameblock@applesandbananas.co.uk",
    description="A pygame framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dw-Apples-And-Bananas/gameblock",
    project_urls={
        "Bug Tracker": "https://github.com/dw-Apples-And-Bananas/gameblock/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "gameblock"},
    packages=setuptools.find_packages(where="gameblock"),
    python_requires=">=3.6",
)
