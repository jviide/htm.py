import setuptools

with open("README.md", "r") as readme:
    long_description = readme.read()

docs_require = [
    'Sphinx',
    'sphinx_rtd_theme',
    'sybil',
]

setuptools.setup(
    name="htm",
    version="0.1.0",
    author="Joachim Viide",
    author_email="jviide@iki.fi",
    description="HTM for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jviide/htm.py",
    packages=setuptools.find_packages(),
    install_requires=["tagged"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    extras_require=dict(docs=docs_require)
)
