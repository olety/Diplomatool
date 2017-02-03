from setuptools import setup
from pip.req import parse_requirements
# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements('requirements.txt')
# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
reqs = [str(ir.req) for ir in install_reqs]

setup(name='ssd-project',
      version='0.1',
      description='ssd project by Oleksii and Piotr',
      author='Oleksii Kyrylchuk, Piotr Fudali',
      author_email='olkyrylchuk@gmail.com',
      install_requires=reqs
      )
