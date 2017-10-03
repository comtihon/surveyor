from setuptools import setup, find_packages

import tester

setup(name='survey_tester',
      version=tester.vsn,
      description='surveyor integration test tool',
      author='Val',
      author_email='valerii.tikhonov@gmail.com',
      packages=find_packages(),
      install_requires=['docopt', 'colorama', 'PyYAML', 'requests', 'kafka', 'pymongo', 'psycopg2'],
      entry_points={
          'console_scripts': [
              'survey_tester=tester.__main__:main'
          ]},
      package_data={'tester': ['resources/*']}
      )
