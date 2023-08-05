from setuptools import find_packages, setup

with open("README.md", "r") as readme:
    long_description = readme.read()

setup(
    name="sfilter",
    version="0.1.1",
    python_requires=">=3.7",
    author="Sasha Bondarev (Oleksandr)",
    author_email="alex.d.bondarev@gmail.com",
    license="MIT",
    description="Tool for filtering out stinky/smelling code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alex-d-bondarev/sfilter",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "black==21.7b0",
        "click==8.0.3",
        "ConfigUpdater==3.0.1",
        "flake8==3.9.2",
        "isort==5.9.2",
        "radon==4.1.0",
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Quality Assurance",
    ],
    entry_points={
        "console_scripts": [
            "sfilter=src.sfilter.cli:main",
        ]
    },
)
