from setuptools import find_packages, setup
setup(
    name='email_lib_setup_name',
    packages=find_packages(include = ['email_lib']),
    version='0.1.0',
    description='My first Python library',
    author='Felix Deichsel',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)