from distutils.core import setup

setup(
    name='Padsniff',
    version='0.1.0',
    description='Command-line tool to sniff Puzzle & Dragons data.',
    author='Will Medlar',
    author_email='wmmedlar@gmail.com',
    packages=['padsniff'],
    entry_points={
        'console_scripts': [
            'padsniff = padsniff.cli:cli'
        ]
    }
)