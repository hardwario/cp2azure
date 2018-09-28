from setuptools import setup

setup(
    name='cp2azure',
    packages=['cp2azure'],
    version='1.0.0',
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
        'Topic :: Scientific/Engineering :: Human Machine Interfaces',
        'Environment :: Console',
        'Intended Audience :: Science/Research'
    ],
    install_requires=[
        'azure-iothub-device-client==1.4.3', 'click==6.7', 'PyYAML==3.13','pyzmq==17.1.2'
    ],
    entry_points='''
        [console_scripts]
        cp2azure=cp2azure.cli:main
    '''
)
