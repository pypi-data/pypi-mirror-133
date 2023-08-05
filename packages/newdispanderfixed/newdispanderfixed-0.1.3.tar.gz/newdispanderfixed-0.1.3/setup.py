import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="newdispanderfixed",
    version="0.1.3",
    author="susi-chaaaan",
    author_email="sushi_code@outlook.jp",
    description="Discord Message URL Expander-fixed for d.py 2.0.0a",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=[
    ],
)
