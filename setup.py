from setuptools import setup, find_packages

setup(
    name='imagefile',
    version="1.0.1",
    description="Utility class to easily manipulate image files.",
    long_description="",
    author='kawazome',
    packages=find_packages(),
    install_requires=[
        'Pillow',
        'piexif'
    ]
)
