import ast
import pathlib
import setuptools

PROJECT_ROOT = pathlib.Path(__file__).parent

def _get_version():
    with open('fleetio/_meta.py') as meta_file:
        for line in meta_file:
            if line.startswith('__version__'):
                return ast.parse(line).body[0].value.value


VERSION = _get_version() or '0.0.1'
README = (PROJECT_ROOT / 'README.md').read_text()

setuptools.setup(
    name='pyfleetio',
    version=VERSION,
    author='Alexandre Bélanger',
    author_email='a.belanger89@gmail.com',
    description="Fleetio's Python API Wrapper Package",
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/AlexBelanger/pyfleetio',
    project_urls={
        "Bug Tracker": "https://github.com/AlexBelanger/pyfleetio/issues",
    },
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={
        '': ['*.json']
    },
    install_requires=[
        'requests', 'ratelimit', 'backoff'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    license='LICENSE',
    python_requires=">=3.7",
)
