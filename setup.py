from setuptools import setup

with open('README.md') as f:
    readme = f.read()

with open('requirements.txt') as f:
    install_requires = f.readlines()

with open('dev-requirements.txt') as f:
    tests_require = install_requires + f.readlines()

setup(
    name='padsniff',
    version='1.0.0',
    description='Command-line tool to sniff Puzzle & Dragons data.',
    long_description=readme,
    url='https://bitbucket.org/necromanteion/padsniff',
    author='Will Medlar',
    author_email='wmmedlar@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
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
    install_requires=install_requires,
    setup_requires=['pytest-runner'],
    tests_require=tests_require,
    packages=['padsniff'],
    entry_points={
        'console_scripts': [
            'padsniff = padsniff.cli:cli'
        ]
    }
)
