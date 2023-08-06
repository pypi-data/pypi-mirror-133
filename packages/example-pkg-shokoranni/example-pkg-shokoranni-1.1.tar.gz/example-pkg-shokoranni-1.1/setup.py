import setuptools, os
setuptools.setup(
    name="example-pkg-shokoranni",  # Replace with your own PyPi
    version="1.1",
    author="Foo Bar",
    author_email="lidor.ettinger@example.com",
    description="A small example package",
    url="https://github.com/naturalett/getting-started",
    packages=['calculate'],
    scripts=['calculate/calc.py'],
    python_requires='>=3.9',
)