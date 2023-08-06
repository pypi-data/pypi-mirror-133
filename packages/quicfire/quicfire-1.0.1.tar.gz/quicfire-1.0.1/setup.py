import pathlib
from setuptools import setup
import subprocess

# Fetch version number from git tag
qf_version = (
    subprocess.run(['git', 'describe', '--tags'], stdout=subprocess.PIPE)
    .stdout.decode('utf-8')
    .strip()
)

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='quicfire',
    packages=['quicfire'],
    version=qf_version,
    license='Proprietary',
    description='Python SDK for the QUIC-Fire API',
    long_description=README,
    long_description_content_type="text/markdown",
    author='Anthony Marcozzi and Lucas Wells, Holtz',
    author_email='anthony@holtztds.com',
    keywords=['fire model', 'simulation', 'wildfire'],
    install_requires=[
        'pydantic',
        'requests',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Programming Language :: Python :: 3',
    ]
)
