from setuptools import setup, find_packages


setup(
    name='amadeuslib',
    version='0.1',
    license='MIT',
    author="Justin",
    author_email='hello@justin681.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/justinl681',
    keywords='amadeus flight travel api',
    install_requires=[
          'requests',
          'json'
      ],
)