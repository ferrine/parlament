from setuptools import setup, find_packages

if __name__ == '__main__':
    setup(
        name='parlament',
        version='0.0.0',
        packages=find_packages(),
        maintainer='Maxim Kochurov',
        maintainer_email='maxim.v.kochurov@gmail.com',
        description='Tool for parlament description',
        license='Apache License, Version 2.0',
        tests_require=['pytest']
    )
