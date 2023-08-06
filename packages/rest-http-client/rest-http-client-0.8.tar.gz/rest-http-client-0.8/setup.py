import setuptools

requirements = [
    'pytest~=6.2.5',
    'requests~=2.27.1',
    'urllib3~=1.26.8',
    'logger-config==0.2',
    'arrow==1.2.1',
]

setuptools.setup(install_requires=requirements)
