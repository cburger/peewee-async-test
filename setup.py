from setuptools import setup, find_packages

setup(
    name='peewee-async-test',
    description='Project to test Peewee Async Testing',
    author='Carel Burger',
    install_requires=[
        'aiohttp ~=2.3.2 ',
        'peewee-async ~=0.5.7',
        'aiopg ~=0.13.1',
        'factory_boy',
        'asynctest',
        'pytest-aiohttp',
        'pytest',
    ],
    version='0.1',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    zip_safe=False,
)
