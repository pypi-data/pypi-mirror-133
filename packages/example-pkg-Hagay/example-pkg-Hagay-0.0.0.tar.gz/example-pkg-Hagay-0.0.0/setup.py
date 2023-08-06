import setuptools, os

setuptools.setup(
    name="example-pkg-Hagay",  # Replace with your own PyPi
    version=os.environ.get("BUILD_VERSION"),
    description="A small example package",
    url="https://github.com/naturalett/getting-started",
    packages=['calculate'],
    scripts=['calculate/calc.py'],
    python_requires='>=3.9',
)
