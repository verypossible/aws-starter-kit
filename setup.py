import os
import glob
from setuptools import setup, find_packages

src_dir = os.path.dirname(__file__)

install_requires = [
    'stacker',
    'stacker_blueprints',
]

tests_require = (
    'pytest',
    'pytest-mock',
    'pytest-cov',
    'flake8',
)


if __name__ == '__main__':
    setup(
        name='aws-infrastructure',
        version='0.1.0',
        description='stacker project for aws-infrastructure',
        install_requires=install_requires,
        tests_require=tests_require,
        packages=find_packages(),
        scripts=glob.glob(os.path.join(src_dir, 'bin', 'scripts', '*'))
    )
