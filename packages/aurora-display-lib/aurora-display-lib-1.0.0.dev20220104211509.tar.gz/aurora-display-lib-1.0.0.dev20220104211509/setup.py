from os.path import abspath, dirname, join
from setuptools import setup, find_packages


HERE = abspath(dirname(__file__))


def _read_file(path: str) -> str:
    """ Reads any file and returns its content as a string """
    with open(path, 'r') as f:
        return f.read()


setup(
    name='aurora-display-lib',
    version='1.0.0-dev20220104211509',
    description='Display library based on PIL/Pillow intended for Raspberry Pi applications running custom displays',
    long_description=_read_file(join(HERE, 'README.md')),
    long_description_content_type='text/markdown',
    author='Raphael "rGunti" Guntersweiler',
    author_email='raphael+pip@gunti.cloud',
    license='MIT',
    url='https://gitlab.com/aurora-display-lib',
    packages=find_packages(include=['aurora', 'aurora.*']),
    python_requires='>=3.5',
    install_requires=[
        'Pillow>=8.4.0',
        'pygame>=2.1.2'
    ],
    extras_require={
        'deploy': [
            'bump2version'
        ],
        'test': [
            'testfixtures>=1.2.0',
            'pytest>=3.4.0',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only'
    ],
    include_package_data=True,
    include_dirs=[
    ],
    entry_points={},
    zip_safe=False)
