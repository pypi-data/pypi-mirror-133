from setuptools import setup, find_packages

setup(
    name='biostarPython',
    version='0.1.0',
    author_email = 'gcartlidge@supremainc.com',
    author = 'SupremaUK',
    url = 'https://github.com/biostar-dev/g-sdk/',
    packages=['biostarPython','biostarPython.service','biostarPython.proto'],
    python_requires='>3.5.2',
    package_data={
        "": ["*.py", "*.proto", "*.json"],
        "proto": ["*.proto"],
        "service": ["*.py"],
    },
    install_requires=[
        'grpcio',
        'protobuf',
    ],
)