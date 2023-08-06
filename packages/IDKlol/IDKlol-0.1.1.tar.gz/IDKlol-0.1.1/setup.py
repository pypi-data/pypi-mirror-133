import setuptools




setuptools.setup(
    name='IDKlol',
    version="0.1.0",
    author="Mathyslol",
    description="test for secret",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'BenBotAsync',
        'FortniteAPIAsync',
        'aiohttp',
        'colorama',
        'crayons',
        'fortnitepy',
        'requests',
        'sanic (==21.6.2)',
        'uvloop'
    ],
)