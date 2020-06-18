from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt', 'r') as f:
    requirements = f.read()

setup(
    name='cp2azure',
    packages=['cp2azure'],
    version='@@VERSION@@',
    description='COOPER to Azure IoT Hub',
    url='https://github.com/hardwario/cp2azure',
    author='HARDWARIO s.r.o.',
    author_email='ask@hardwario.com',
    license='MIT',
    keywords = ['cooper', 'azure', 'iot'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Human Machine Interfaces',
        'Environment :: Console',
        'Intended Audience :: Science/Research'
    ],
    install_requires=requirements,
    entry_points='''
        [console_scripts]
        cp2azure=cp2azure.app:main
    ''',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
