import setuptools

with open("README", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytasking",
    version="1.2.0",
    author="Jason Zi Feng Lei",
    author_email="TokenChingy@gmail.com",
    description="A multitasking library for Python 3.5+",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TokenChingy/pytasking",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
