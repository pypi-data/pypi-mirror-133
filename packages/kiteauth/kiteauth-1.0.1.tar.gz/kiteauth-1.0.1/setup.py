from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
]

setup(
    name='kiteauth',
    version='1.0.1',
    description='Kite authentication library',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='@vatadepalli',
    author_email='info@integriert.com',
    license='MIT',
    classifiers=classifiers,
    keywords='kite authentication',
    packages=find_packages(),
    install_requires=['kiteconnect', 'selenium']
)