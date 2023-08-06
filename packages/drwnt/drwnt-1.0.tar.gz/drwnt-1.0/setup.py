from setuptools import setup,find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='drwnt',
    version='1.0',
    description='Simple library to draw neural networks using pygame.',
    long_description=open('README.txt').read()+'\n\n'+open('CHANGELOG.txt').read(),
    url='',
    author='Jakub Kubin, Karafak',
    author_email='karafak7@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='Neural Network, AI, NN',
    packages=find_packages(),
    install_requires=['pygame']
)