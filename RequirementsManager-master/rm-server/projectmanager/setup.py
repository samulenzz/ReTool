from setuptools import setup, find_namespace_packages


setup(
    name="projectmanager",
    version="0.0.1",
    packages=find_namespace_packages(),
    install_requires=[
        'flask',
        'flask_cors',
        'pymongo',
        'tornado',
        'requests',
    ]
)
