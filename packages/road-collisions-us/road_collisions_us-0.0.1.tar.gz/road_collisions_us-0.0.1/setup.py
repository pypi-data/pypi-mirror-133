from setuptools import (
    find_packages,
    setup
)

INSTALL_REQUIRES = (
    'road-collisions-base',
    'boto3'
)

setup(
    name='road_collisions_us',
    version='0.0.1',
    python_requires='>=3.6',
    description='Road collision data for the United States',
    author='Robert Lucey',
    url='https://github.com/RobertLucey/road-collisions-us',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=INSTALL_REQUIRES,
    entry_points={
        'console_scripts': [
            'load_road_collisions_us = road_collisions_us.bin.load:main',
        ]
    }
)
