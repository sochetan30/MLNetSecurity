'''
setup.py : 
    - Essential part of packaging and sistributing python projects.
    - It is used by setuptools to define the configuration suche as metadata, 
    dependencies and more
'''

from setuptools import find_packages, setup
from typing import List
#find_packages: scans all project and checks for __init__.py file and consider this as part of package
#setup : Responsible to provide project info.

def get_requirements()-> List[str]:
    """
    This Fucntion will return list of requirements
    """
    requirement_lst=[]
    try:
        with open('requirements.txt', 'r') as file:
            #Read lines from the file
            lines =file.readlines()

            ## Process Each line
            for line in lines:
                requirement=line.strip()

                ##ignore empty lines and -e .

                if requirement and requirement!='-e .':
                    requirement_lst.append(requirement)

    except FileNotFoundError:
        print("requirements.txt file is not found.")

    return requirement_lst


setup(
    name='MLNetSecurity',
    version="0.0.1",
    author='Chetan Solanke',
    author_email='chetantrust30@gmail.com',
    packages=find_packages(),
    install_requirements=get_requirements()
)
