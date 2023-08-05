import setuptools
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()
    
    
setuptools.setup(
  include_package_data=False,
  name='DeepNeuralBranchNet',
  version='0.0.14',
  url='https://github.com/hamzahshabbir96/Neural-network-with-branching-output',
  description='Neural network module with branching output',
  author='Hamzah Shabbir',
  author_email='hamzahshabbir7@gmail.com',
  packages=setuptools.find_packages(),
  install_requires=['numpy'],
  long_description=long_description,
  long_description_content_type='text/markdown',
  keywords=['Neural Network','Classification','Python','Neurons','layers'],
   classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'Topic :: Software Development',
          'Topic :: Scientific/Engineering :: Artificial Intelligence',
          'Topic :: Scientific/Engineering',
       'Topic :: Scientific/Engineering :: Artificial Life',
      ]
  


)
