from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='spicesor',
  version='0.0.1',
  description='A library or package to slice sparse tensors with one, two, or three dimensions',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
  long_description_content_type = 'text/markdown',
  url='https://github.com/andreasbrownethz/ISC2021-solutions/tree/main/assignment_8',  
  author='Andreas Brown',
  author_email='browna@student.ethz.ch',
  license='MIT', 
  classifiers=classifiers,
  keywords=['spicesor', 'slice', 'sparse', 'tensor'], 
  packages=find_packages(),
  install_requires=['numpy', 'tensorflow'] 
)