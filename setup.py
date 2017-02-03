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
            'django',
            'django-crispy_forms',
            'django-model-utils'
          ],
      )