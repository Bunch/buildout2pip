from setuptools import setup, find_packages


setup(
    name='buildout2pip',
    version=0.1,
    author='Hany Fahim',
    author_email='hany@vmfarms.com',
    url='https://github.com/hany55/buildout2pip',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points={
          'console_scripts': [
              'buildout2pip = buildout2pip:main',
          ]},
)
