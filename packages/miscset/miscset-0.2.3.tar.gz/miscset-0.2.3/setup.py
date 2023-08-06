import setuptools
from miscset._version import version

setuptools.setup(
    name = "miscset",
    version = version,
    author = "Sven Templer",
    author_email = "sven.templer@gmail.com",
    description = "Miscellaneous set of helpful methods.",
    long_description = open("README.md", encoding = "utf-8").read(),
    long_description_content_type = "text/markdown",
    url = "https://miscset.readthedocs.org",
    packages = setuptools.find_packages(),
    classifiers = [
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Topic :: System :: Shells",
        "Topic :: Utilities",
        "Topic :: Text Processing :: Markup :: HTML"
    ],
    #install_requires = miscset.io.read_lines("requirements.txt"),
    install_requires = open("requirements.txt").readlines(),
    python_requires = ">=3.6",
)
