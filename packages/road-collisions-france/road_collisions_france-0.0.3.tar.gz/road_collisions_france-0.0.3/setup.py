from setuptools import (
    find_packages,
    setup
)

INSTALL_REQUIRES = (
    'road-collisions-base'
)

setup(
    name='road_collisions_france',
    version='0.0.3',
    python_requires='>=3.6',
    description='Road collision data for France',
    author='Robert Lucey',
    url='https://github.com/RobertLucey/road-collisions-france',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=INSTALL_REQUIRES,
    package_data={
        'road_collisions_france': [
            'resources/fr/fr.csv.tgz'
        ]
    },
    entry_points={
        'console_scripts': [
            'load_road_collisions_france = road_collisions_france.bin.load:main',
        ]
    }
)
