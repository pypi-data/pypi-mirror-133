from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='CheckRequest',
  version='0.0.1',
  description='A connection checker',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Algrow',
  author_email='nobody@needsit.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='connection', 
  packages=find_packages(),
  install_requires=['requests', 'beautifulsoup4']
)