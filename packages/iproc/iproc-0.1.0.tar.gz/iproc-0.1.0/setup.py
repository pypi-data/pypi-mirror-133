from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="iproc",
    version="0.1.0",
    author="Joseph Diza",
    author_email="josephm.diza@gmail.com",
    description="Simple image processing scripts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jmdaemon/iproc",
    project_urls={
        "Bug Tracker": "https://github.com/jmdaemon/iproc/issues",
    },
    license='MIT',
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
    py_modules=[],
    install_requires=[
        'argparse',
    ],
    entry_points={
        'console_scripts': [
            'iproc = iproc.cli:main',
        ],
    },
    test_suite='tests',
)
