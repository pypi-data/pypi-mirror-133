from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='simple_hello_app',
    version='0.0.1',
    description='hello_app',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='moti ksir',
    author_email='motiksir@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='simple_hello_app',
    packages=find_packages(),
    install_requires=['']
)