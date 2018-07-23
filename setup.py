from setuptools import setup

setup(name='drexel_med_h_and_e_normalization',
      version='0.1',
      description='Creates normalized H&E histology images',
      install_requires=[
          'sklearn',
          'numpy',
          'imageio',
      ],
      packages=['h_and_e_normalization'])