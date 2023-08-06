from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='funnyiest',
      version='0.2',
      description='The funniest joke in the world',
      url='http://github.com/storborg/funniest',
      author='Flying Circus',
      install_requires = ['markdown'],
      author_email='flyingcircus@example.com',
      license='MIT',
      packages=['funnyiest'],
      zip_safe=False)
