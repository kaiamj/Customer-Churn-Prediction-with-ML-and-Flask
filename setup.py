# responsible to make ml model a package
# anyone can install this ml model as package and can build pipleline

from setuptools import find_packages, setup
from typing import List
HYPEN_E = '-e .'
def get_requirements(file_path:str)->List[str]:
    '''
    func will return list of required libraries
    '''
    requirement = []
    with open(file_path) as f:
        requirement = f.readlines()
        requirement =  [req.replace ("\n","") for req in requirement]

        if HYPEN_E in requirement:
            requirement.remove(HYPEN_E)
    return requirement

setup(
    name = "mlproject",
    version = '0.0.1',
    author = 'kainaa',
    author_email = 'kainaat562@yahoo.com',
    packages= find_packages(), # number of packages it will detect depends on folders with __init__.py file
    install_requires = get_requirements('requirements.txt') #for more libraries 

)