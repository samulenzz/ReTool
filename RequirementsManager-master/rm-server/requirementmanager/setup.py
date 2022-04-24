from setuptools import setup, find_namespace_packages


setup(
    name="requirementmanager",
    version="0.0.1",
    packages=find_namespace_packages(),
    install_requires=[
        'flask',
        'flask_cors',
        'pymongo',
        'python-docx',
        'tornado',
        'grpcio',
        'protobuf',
        'requests',
    ]
)
