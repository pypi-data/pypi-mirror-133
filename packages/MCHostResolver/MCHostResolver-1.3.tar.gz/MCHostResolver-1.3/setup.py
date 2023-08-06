import setuptools

setuptools.setup(
    name='MCHostResolver',
    version='1.3',
    packages=['MCHostResolver'],
    url='https://github.com/itskek/MCHostResolver',
    license='MIT',
    author='itskekoff',
    author_email='itskekoff@gmail.com',
    description='A module for resolving MC hostnames',
    install_requires=['colorama', 'dnspython']
)
