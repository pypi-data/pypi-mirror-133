import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mptimer",
    version=open('/home/runner/Timer/version.ver','r').read(),
    author="Github73840134 (Pytech Software)",
    author_email="",
    description="Timer is module ported from micropython's machine.Timer and adapted to work with Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Github73840134/Timer",
    project_urls={
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "Timer"},
    packages=setuptools.find_packages(where="Timer"),
    python_requires=">=3.6",
)