import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="modularcalculator",
    version="1.4.0.999",
    author="Jordan Leppert",
    author_email="jordanleppert@gmail.com",
    description="A library to add a heavily customisable calculator to your application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JordanL2/ModularCalculator",
    packages=setuptools.find_packages() + setuptools.find_namespace_packages(include=['modularcalculator.*']),
    install_requires=[
        'scipy',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: LGPL-2.1 License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
