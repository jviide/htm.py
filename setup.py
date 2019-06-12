import setuptools

with open("README.md", "r") as readme:
    long_description = readme.read()

setuptools.setup(
    name="htm",
    version="0.0.1",
    author="Joachim Viide",
    author_email="jviide@iki.fi",
    description="HTM for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jviide/htm.py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
