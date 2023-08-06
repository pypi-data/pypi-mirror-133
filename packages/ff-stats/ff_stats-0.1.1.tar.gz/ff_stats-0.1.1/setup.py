from setuptools import setup, find_packages

setup(
      description = 'A package to pull fantasy football projections.',
      name = 'ff_stats',
      author = 'Patrick McCullough',
      version = '0.1.1',
      packages = find_packages(),
      python_requires = '>=3',
      install_requires = ['pandas>1.0.0', 'requests>=2.0.0'],
      classifiers = [
          'Programming Language :: Python :: 3',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent'])


