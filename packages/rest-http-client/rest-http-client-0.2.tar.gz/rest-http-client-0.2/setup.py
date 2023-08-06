import sys

import setuptools


def get_requirements(filename):
    try:
        with open(filename, 'r') as fd:
            packages = fd.read().split('\n')
            packages = list(filter(lambda x: x or not x.startswith('#') or not x.startswith(' '), packages))
            return packages

    except Exception as ex:
        sys.exit('Could not find requirements.txt \nException: {}'.format(ex))


setuptools.setup(install_requires=get_requirements('./requirements.txt'))
