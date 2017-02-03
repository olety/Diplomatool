from setuptools import setup

setup(name='ssd-project',
      version='0.1',
      description='ssd',
      long_description='ssd project by Oleksii and Piotr',
      author='Oleksii Kyrylchuk, Piotr Fudali',
      author_email='olkyrylchuk@gmail.com',
      license='None',
      zip_safe=False,
      install_requires=[
          'Django',
          'django-crispy-forms',
          'django-model-utils',
          'pbr',
          'Pygments',
          'requests',
          'six',
          'stevedore',
          'tabulate',
          'virtualenv',
          'virtualenv-clone',
          'virtualenvwrapper',
          'wheel'
      ],
      )
