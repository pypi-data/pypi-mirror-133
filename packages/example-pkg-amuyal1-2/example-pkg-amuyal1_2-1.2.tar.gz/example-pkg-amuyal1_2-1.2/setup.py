import setuptools, os
setuptools.setup(
    name="example-pkg-amuyal1_2",  # Replace with your own PyPi
    version="1.2",
    author="Foo Bar",
    author_email="amuya@example.com",
    description="A small example package",
    url="https://github.com/naturalett/getting-started",
    packages=['calculate'],
    scripts=['calculate/calc.py'],
    python_requires='>=3.9',
)
