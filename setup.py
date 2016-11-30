from setuptools import setup

with open('requirements.txt') as f:
    requires = f.readlines()

setup(
    name='padsniff',
    version='0.9.2',
    description='Command-line tool to sniff Puzzle & Dragons data.',
    url='https://bitbucket.org/necromanteion/padsniff',
    author='Will Medlar',
    author_email='wmmedlar@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Games/Entertainment :: Puzzle Games',
    ],
    keywords=[
        'puzzle & dragons',
        'man-in-the-middle',
        'reverse engineering',
    ],
    install_requires=requires,
    packages=['padsniff'],
    entry_points={
        'console_scripts': [
            'padsniff = padsniff.cli:cli'
        ]
    }
)
