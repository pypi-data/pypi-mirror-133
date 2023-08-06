from setuptools import setup, find_packages
clasifiers=[
    'Development Status::5-Production/Stable',
    'Intended Audience::Education',
    'Operating System::Microsoft::Windows::Windows 10',
    'License::OSI Approved::MIT License',
    'Programming Language::Python::3'
    
    ]
setup(
      name='Mariam Eristavi',
      version='0.0.1',
      description="Simple Calculator",
      long_description=open('README.txt').read()+'\n\n'+open('CHANGELOG.txt').read(),
      url='',
      Author='Mariam Eristavi',
      Author_Email='Mariami.Eristavi.1@btu.edu.ge',
      license='MIT',
      keywords='Calculator',
      packages=find_packages(),
      install_require=['']
      
      )
