from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='easywork',
    version='0.0.3',
    author='paomianplus',
    author_email='paomianplus@foxmail.com',
    url='https://www.paomian.plus',
    install_requires=['fake_useragent==0.1.11', 'python_dateutil==2.8.2', 'requests==2.27.0', 'setuptools==58.0.4'],
    long_description=long_description,
    packages=find_packages()
)
