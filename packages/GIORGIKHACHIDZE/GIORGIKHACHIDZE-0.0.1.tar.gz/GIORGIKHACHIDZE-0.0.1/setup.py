from setuptools import setup, find_packages
classifiers=[
    'Development Status::5-Production/Stable',
    'Intended Audience::Education',
    'Operating System::Microsoft::Windows::Windows 10 ',
    'License::OSI Approved::MIT License',
    'Programminf Language::Python::3'
     
    ]
setup(
      name='GIORGIKHACHIDZE',
      version='0.0.1',
      description="simple Calculator",
      long_description=open('README.txt').read()+'\n\n'+open('CHANGELOG.txt').read(),
      url='',
      author='GIORGI KHACHIDZE',
      author_email='giorgi.khachidze.1@btu.edu.ge',
      license='MIT',
      keywords='calculator',
      packages=find_packages(),
      install_require=['']
      )