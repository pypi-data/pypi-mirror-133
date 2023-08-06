from setuptools import setup

setup(
    name='kafkautil-ecs',
    version='1.0.0',
    py_modules=['kafkautil'],
    author="Ryan Gilmore",
    author_email = "ryan.gilmore@ecstech.com",
    long_description="Python Package for testing kafka connections",
    install_requires=[
        'Click',"kafka-python"
    ],
    entry_points={
        'console_scripts': [
            'kafkautil = kafkautil:cli',
        ],
    },
    classifiers=[
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
    ],
)