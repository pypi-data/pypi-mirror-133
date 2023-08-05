######################################################
##  SihinaCode > Search YouTube for more tutorials  ##
######################################################

from setuptools import setup

long_description = open('README.MD').read()
setup(
  name = 'sc_mainwindow',
  packages = ['sc_mainwindow', 'sc_mainwindow.components'],
  version = '1.2',
  license='MIT',
  description = 'sc_mainwindow is a pyqt5 custom widget.',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'SihinaCode',
  url = 'https://github.com/SihinaCode/sc_mainwindow',
  download_url = 'https://github.com/SihinaCode/sc_mainwindow',
  keywords = ['pyqt5', 'mainWindow', 'frameless'],
  zip_ok = False,
  install_requires=[ 
          'pyqt5',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)