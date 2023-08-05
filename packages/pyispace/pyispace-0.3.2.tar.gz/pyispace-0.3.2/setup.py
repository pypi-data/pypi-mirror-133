from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pyispace',
    version='0.3.2',
    description='Python Instance Space Analysis package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['pyispace'],
    url='https://gitlab.com/ita-ml/pyispace',
    download_url='https://gitlab.com/ita-ml/pyispace/-/archive/v0.3.2/pyispace-v0.3.2.tar.gz',
    license='MIT',
    author='Pedro Paiva',
    author_email='paiva@ita.br',
    install_requires=[
        'numpy>=1.18.5',
        'scipy>=1.5.4',
        'scikit-learn>=0.23.1',
        'shapely>=1.7.1',
        'pandas>=1.1',
        'alphashape>=1.3.1'
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    entry_points={'console_scripts': ['isa=pyispace.cli:main']}
)
