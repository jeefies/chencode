from setuptools import setup

# from blog.csdn.net/tcy23456/article/details/91886555

with open('README.md') as f:
    long_des=f.read()

with open('requirements.txt') as f:
    reqs = f.read().strip().split()

setup(
        name = 'chencode',
        author = 'Jeefy',
        version = '0.0.1',
        packages = ['chencode'],
        author_email = 'jeefy163@163.com',
        description = 'A easy method to encrypt/decrypt chinese letters based on thier PinYin',
        python_requires = '>3.4',
        url = 'https://github.com/jeefies/chencode',
        long_description = long_des,
        long_description_content_type = 'text/markdown',
        install_requires = [reqs]
        )
