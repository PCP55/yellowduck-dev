import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yellowduck", 
    version="0.1.0",
    author="Chalat Phumphiraratthaya",
    author_email="chalat.phum@gmail.com",
    description="Data Science Toolbox for everyone",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PCP55/yellowduck",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)