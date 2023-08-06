from distutils.core import setup

setup(
  name = 'shahienetal',
  packages = ['shahienetal'],
  version = '1',  # Ideally should be same as your GitHub release tag varsion
  description = 'description',
  license='MIT',
  author = 'Abdulrhman Shahien',
  author_email = 'abdopetroleum@gmail.com',
  url = 'https://github.com/abdopetroleum/ShahienBeggs',
  install_requires=[
    'pandas',
    'numpy',
    'scipy',
    'seaborn',
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)