import setuptools, os

setuptools.setup(
    name="example-pkg-pavelg48",  # Replace with your own PyPi
    version="1.1",
    author="JerLion",
    author_email="pavelg48@example.com",
    description="A first small example package",
    url="https://github.com/naturalett/getting-started",
    packages=['calculate'],
    scripts=['calculate/calc.py'],
    python_requires='>=3.9',
)