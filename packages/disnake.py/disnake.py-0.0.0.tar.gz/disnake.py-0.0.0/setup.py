from setuptools import setup


with open("README.md", encoding="utf-8") as f:
    readme = f.read()


setup(
    name="disnake.py",
    author="shiftinv",
    long_description=readme,
    long_description_content_type="text/markdown",
)
