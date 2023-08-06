import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='MCHostResolver',
    version='1.5',
    packages=['MCHostResolver'],
    url='https://github.com/itskek/MCHostResolver',
    license='MIT',
    author='itskekoff',
    author_email='itskekoff@gmail.com',
    description='A module for resolving MC hostnames',
    install_requires=['colorama', 'dnspython'],
    long_description = long_description,
    long_description_content_type = "text/markdown"
)
