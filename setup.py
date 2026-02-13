'''
   This setup file is essentialfor packaging and distributing the package. 
'''
   
from setuptools import setup, find_packages
from typing import List

def get_requirements() -> List[str]:
    '''
    This function return the list of requirements
    '''
    requirements = []
    try:
       with open('requirements.txt', 'r') as file: 
           lines = file.readlines()
           for line in lines:
               line = line.strip()
               if line and not line.startswith('-e .'):
                   requirements.append(line)
    except FileNotFoundError as e:
        print("requirement.txt file not found")
        
    return requirements    


setup(
    name='NetworkSecurity',
    version='0.0.1',
    author='Ajay',
    author_email='ajaykm000563@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements()
)
