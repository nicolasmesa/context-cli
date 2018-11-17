import setuptools

import context_cli

with open("README.md", "r") as fh:
    long_description = fh.read()

test_require = [
    'pytest',
]
setup_requires=[
    'pytest-runner',
]

setuptools.setup(
    name="context-cli",
    version=context_cli.__version__,
    author=context_cli.__author__,
    author_email="nicolasmesa@gmail.com",
    description=context_cli.__doc__.strip(),
    license=context_cli.__licence__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nicolasmesa/context-cli",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'ctx = context_cli.__main__:main',
        ],
    },
    test_suite='tests',
    tests_require = test_require,
    setup_requires=setup_requires,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'Topic :: System :: Networking',
        'Topic :: Terminals',
        'Topic :: Text Processing',
        'Topic :: Utilities',
    ],
)
