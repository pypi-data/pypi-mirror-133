from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'Operating System :: Microsoft :: Windows',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='InfoMarketClientApp',
    version='0.0.4',
    description='Information Market client application',
    long_description='Information Market client application to request data from the Information Market servers',
    url='',
    author='Ricardo Martins',
    author_email='ricas.martins767@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='InformationMarket',
    py_modules=["IMClient"]
)