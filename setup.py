import setuptools

setuptools.setup(
    name = 'unichem',
    version = '0.1.0',
    author = 'Daniel Himmelstein',
    author_email = 'daniel.himmelstein@gmail.com',
    url = 'https://github.com/dhimmel/obo',
    description = 'OBO ontology tools in python',
    license = 'CC0',
    py_modules = ['unichem'],
    install_requires = ['requests'],
    )
