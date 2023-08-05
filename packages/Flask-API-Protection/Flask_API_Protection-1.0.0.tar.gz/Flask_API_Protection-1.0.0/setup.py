from distutils.core import setup

setup(
    name='Flask_API_Protection',
    version='1.0.0',
    py_modules=['api_protection', 'auth'],
    author='wangzirui32',
    author_email='wangzirui32@163.com',
    description='Flask API保护',
    install_requires=['flask']
)