import setuptools, os

setuptools.setup(
    name="example-pkg-slavapas13",  # Replace with your own PyPi
    version='1.0',
    author="Foo Bar",
    author_email="slavapas13@gmail.com ",
    description="A small example package",
    url="https://github.com/naturalett/getting-started",
    packages=['calc'],
    scripts=['calc/calculator.py'],
    python_requires='>=3.9',
)
