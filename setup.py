from distutils.core import setup

setup(
    name='padsniff',
    version='0.1.0',
    description='Command-line tool to sniff Puzzle & Dragons data.',
    author='Will Medlar',
    author_email='wmmedlar@gmail.com',
    install_requires=[
        'click==6.6',
        'mitmproxy==0.18.2',
    ],
    packages=['padsniff'],
    entry_points={
        'console_scripts': [
            'padsniff = padsniff.cli:cli'
        ]
    }
)
