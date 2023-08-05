from setuptools import setup

setup(
        name='gamezip64',
        author='Adam Jenca',
        author_email='jenca.a@gjh.sk',
        description='microbit Kitronik Game ZIP 64 plugin',
        py_modules=['gamezip64'],
        entry_points={'console_scripts':['gz64=gamezip64:main']},
        )
