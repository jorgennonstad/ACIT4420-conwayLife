from setuptools import setup, find_packages

setup(
    name="conwayLife",
    version="0.1.0",
    packages=find_packages(),
    py_modules=['main'],
    include_package_data=True,
    package_data={
        "conwayLife": ["patterns/*.txt", "logs/*"]
    },
    entry_points={
        'console_scripts': [
            'conway=main:main',
        ],
    },
)
