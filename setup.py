from runpy import run_path
from setuptools import find_packages, setup

with open('requirements.txt') as f:
    install_requires = f.readlines()

with open('dev-requirements.txt') as f:
    tests_require = install_requires + f.readlines()

setup(
    name='padsniff',
    packages=find_packages(),
    version=run_path('padsniff/meta.py').get('version'),
    description='Command-line tool to sniff Puzzle & Dragons data.',
    url='https://github.com/puzzlluminati/padsniff',
    author='Puzzlluminati',
    author_email='puzzlluminati@gmail.com',
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
    setup_requires=[
        'pytest-runner',
    ],
    python_requires='>=3',
    install_requires=install_requires,
    tests_require=tests_require,
    entry_points={
        'console_scripts': [
            'padsniff = padsniff.cli:cli'
        ]
    }
)
