from setuptools import setup, find_packages

setup(
    name='oneid-jwt-auth-python27',
    version='0.0.1',
    description='oneid-jwt-auth-python27',
    author='oneid',
    author_email='',
    packages=find_packages(),
    install_requires=[
        'PyJWT==1.7.1',
        'cryptography==3.3.2'
    ],
    python_requires='>=2.7, <3.0',
    classifiers=[
        "Programming Language :: Python :: 2.7",
    ]
)
