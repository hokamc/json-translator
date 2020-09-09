from setuptools import setup

setup(
    name='json-translator',
    version='1.0.0',
    description='A json translator for localization',
    author='Man Foo',
    author_email='hokamc00@gmail.com',
    scripts=["src/translator.py"],
    install_requires=['googletrans'],
)