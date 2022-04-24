from setuptools import setup, find_namespace_packages


setup( 
    name = "gateway",
    version = "0.0.1",
    packages = find_namespace_packages(),
    install_requires = [
        'flask',
        'flask_cors',
        'requests',
        'tornado',
    ]
)
