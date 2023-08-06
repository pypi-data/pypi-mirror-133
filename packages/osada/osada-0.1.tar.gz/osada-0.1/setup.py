from setuptools import setup
import osada.__init__ as osada


name = "osada"
author = "Osada Masashi"
author_email = "osadamasashi.c@gmail.com"
maintainer = "Osada Masashi"
maintainer_email = "osadamasashi.c@gmail.com"
description = "osada: It has some useful features to solve what I usually find troublesome. Please use it if you like."
license = "MIT License"
url = "https://github.com/Osada-M/osada"
version = osada.__version__
download_url = "https://github.com/Osada-M/osada"
python_requires = ">=3.6"
# install_requires = []
# extras_require = []
packages = ["osada"]
classifiers = [
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3 :: Only',
    ]

with open("README.rst", "r", encoding="utf8") as f:
    long_description = f.read()


setup(name=name,
      author=author,
      author_email=author_email,
      maintainer=maintainer,
      maintainer_email=maintainer_email,
      description=description,
      long_description=long_description,
      license=license,
      url=url,
      version=version,
      download_url=download_url,
      python_requires=python_requires,
    #   install_requires=install_requires,
    #   extras_require=extras_require,
      packages=packages,
      classifiers=classifiers
    )