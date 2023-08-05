import setuptools

with open("README.md", "r") as readme:
    readme_text = readme.read()

setuptools.setup(
    name="terminalcmd",
    version="0.7.0",
    author="Dallas",
    author_email="aleksey.c5@yandex.ru",
    description="\n",
    long_description=readme_text,
    long_description_content_type="text/markdown",
    url="https://github.com/DarkJoij/terminalcmd",
    packages=["terminalcmd"],
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
