from setuptools import find_packages, setup

setup(
    name='wow-guilds',
    version='0.0.1',
    packages=find_packages(),
    python_requires='>=3.7, <4',
    install_requires=[
        'python-blizzardapi',
        'raiderio',
        'tabulate',
    ],
    entry_points={
        'console_scripts': ['enlightened-rep=wowguilds.runners.enlightened_rep:main']
    },
)
