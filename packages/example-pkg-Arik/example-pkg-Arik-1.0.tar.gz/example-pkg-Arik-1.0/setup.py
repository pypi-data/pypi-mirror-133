import setuptools, os
setuptools.setup(
    name="example-pkg-Arik",  # Replace with your own PyPi
    version="1.0",
    author="Foo Bar",
    author_email="ariklevy.al@example.com",
    description="A small example package",
    url="https://github.com/naturalett/getting-started",
    packages=['calculate'],
    scripts=['calculate/calc.py'],
    python_requires='>=3.9',
)