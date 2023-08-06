import setuptools, os

setuptools.setup(
    name="izzyXYZ",  # Replace with your own PyPi
    version=("1.0"),
    author="izzy",
    author_email="izzy@example.com",
    description="A small example package",
    url="https://github.com/naturalett/getting-started",
    install_requires=['distribution-Final', 'boto3'],
    packages=['calculate'],
    scripts=['calculate/calc.py'],
    python_requires='>=3.9',
)