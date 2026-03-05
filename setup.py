"""setuptools ベースの互換パッケージ設定。"""

from setuptools import find_packages, setup

setup(
    name='jetline',
    version='2020.1',
    packages=find_packages(include=['jetline', 'jetline.*']),
    url='',
    license='MIT',
    author='Katsuya Iwayama',
    author_email='iwayamak@matsubabreak.com',
    description='Application framework for ETL processing.',
    entry_points={
        'console_scripts': [
            'jetline=jetline.cli:main',
        ]
    }
)
