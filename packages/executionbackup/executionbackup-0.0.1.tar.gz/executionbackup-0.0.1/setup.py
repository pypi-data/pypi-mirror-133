from setuptools import setup

setup(
    name='executionbackup',
    version='0.0.1',
    author='TennisBowling',
    author_email='tennisbowling@tennisbowling.com',
    packages=['executionbackup'],
    url='https://github.com/TennisBowling/executionbackup',
    license='LICENSE.md',
    description='An Ethereum execution client switcher',
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    python_requires=">=3.7",
    install_requires=[
        'aiohttp',
        'asyncio',
        'sanic'
    ],
)