from setuptools import setup

setup(name="Grundtvig TEI Parser",
    version="0.0.1",
    author="OliverJarvis@CHCAA",
    description = ("A parser to output metadata and raw text from the Grundtvig Centers TEI fiels."),
    install_requires = [
        'docopt',
        'json',
        'lxml',
        'glob'
    ],
    entry_points={
        'console_scripts': [
            'grundtvigparse = grundtvigparser.__main__:main'
        ]
    }
    )