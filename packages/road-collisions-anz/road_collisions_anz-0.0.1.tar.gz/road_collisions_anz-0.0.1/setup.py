from setuptools import (
    find_packages,
    setup
)

INSTALL_REQUIRES = (
    'road-collisions-base'
)

setup(
    name='road_collisions_anz',
    version='0.0.1',
    python_requires='>=3.6',
    description='Road collision data for Australia and New Zealand',
    author='Robert Lucey',
    url='https://github.com/RobertLucey/road-collisions-anz',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=INSTALL_REQUIRES,
    package_data={
        'road_collisions_anz': [
            'resources/anz/anz.csv.tgz'
        ]
    },
    entry_points={
        'console_scripts': [
            'load_road_collisions_anz = road_collisions_anz.bin.load:main',
        ]
    }
)
