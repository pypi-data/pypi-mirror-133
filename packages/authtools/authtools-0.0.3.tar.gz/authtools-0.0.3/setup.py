from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 3 - Alpha',
  'Intended Audience :: Developers',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='authtools',
  version='0.0.3',
  py_modules=['authtools'],
  description='A Simple CLI Authentication System for Python',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='https://github.com/SavageDevelopment/Savage-AuthTools',  
  author='SavageDevelopment',
  author_email='support@savagesmusic.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='authentication', 
  packages=find_packages(),
)