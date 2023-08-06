from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='time_converters',
  version='1.6.9',
  description='Converts e.g. 24h to 86400',
  long_description=open('README.rst').read(),
  url='https://skayus.pl/',  
  author='Skayuś',
  author_email='skayuus@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='time convert hour second',
  packages=find_packages(),
  install_requires=[] 
)