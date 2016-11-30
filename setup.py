from setuptools import setup

setup(
    name='padsniff',
    version='0.9.0',
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
        'Topic :: Communications :: Chat :: Internet Relay Chat',
        'Topic :: Games/Entertainment :: Puzzle Games',
    ],
    keywords='irc puzzle dragons',
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
