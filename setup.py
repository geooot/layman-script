from setuptools import setup, find_packages
import shutil
import os
print("copying wordbank into root", os.sep)
try:
	shutil.copytree("wordbank", os.sep + "wordbank")
except Exception as e:
	print(e)
setup(name='layman-script',
      version='0.1',
      description='A sentance parser that identifies subjects and verbs and stores them into memory',
      url='https://github.com/geooot/layman-script',
      author='George (geooot) Thayamkery',
      author_email='(0_o)',
      license='MIT',
      packages=find_packages(),
      zip_safe=False,
      include_package_data=True,
      scripts=['bin/layman'])