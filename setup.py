from setuptools import find_packages, setup

with open('requirements.txt') as f:
    install_requires = f.readlines()

with open('dev-requirements.txt') as f:
    tests_require = install_requires + f.readlines()

setup(
    name='padsniff',
    version='1.2.0',
    description='Command-line tool to sniff Puzzle & Dragons data.',
    long_description_markdown_filename='README.md',
    url='https://gitlab.com/wmedlar/padsniff',
    author='Will Medlar',
    author_email='will.medlar@gmail.com',
    license='MIT',
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
    setup_requires=[
        'pypandoc',
        'pytest-runner',
        'setuptools-markdown',
    ],
    tests_require=tests_require,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'padsniff = padsniff.cli:cli'
        ]
    }
)
