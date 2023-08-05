import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
   name='cutegremlin',
   version='1.0.8',
   description='A bunch of painfully dull helpers for AWS and others resources.',
   license='MIT',
   long_description=README,
   long_description_content_type='text/markdown',
   url='https://github.com/JesseZhong/cutegremlin',
   author='Jesse',
   author_email='jessetakuto@gmail.com',
   packages=[
       'gremlin',
       'gremlin.aws',
       'gremlin.web',
       'gremlin.google',
       'gremlin.discord'
    ],
   install_requires=[
       'boto3',
       'requests',
       'discord.py'
    ]
)
