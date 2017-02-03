from setuptools import setup

setup(name='ssd-project',
      version='0.1',
      description='ssd project by Oleksii and Piotr',
      author='Oleksii Kyrylchuk, Piotr Fudali',
      author_email='olkyrylchuk@gmail.com',
      install_requires=[
          'Django',
          'django-crispy-forms',
          'django-model-utils',
          'pbr',
          'Pygments',
          'requests',
          'six',
          'stevedore',
          'wheel'
      ],
      )
