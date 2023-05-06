import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

extras_require = {
    "text": [
        "fuzzywuzzy>=0.18.0",
        "pythainlp>=2.3.2",
        "strsimpy>=0.2.1",
    ],
    "image": [
        "cryptography>=36.0.2",
        "pycryptodome>=3.9.7",
    ],
}

extras_require["full"] = [
    pkg for name in extras_require for pkg in extras_require[name]
]

setuptools.setup(
    name="yellowduck",
    version="1.1.0",
    author="Chalat Phumphiraratthaya",
    author_email="chalat.phum@gmail.com",
    description="Data Science Toolbox for everyone",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PCP55/yellowduck",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering",
    ],
    python_requires=">=3.6",
    install_requires=[
        "black>=22.12.0",
        "flake8>=6.0.0",
        "pep8-naming>=0.13.3",
        "isort>=5.11.5",
        "pre-commit>=2.21.0",
        "scikit-learn>=1.0.0",
    ],
    extras_require=extras_require,
    include_package_data=True,
)
