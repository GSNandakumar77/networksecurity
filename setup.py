"""
setup file essential part of packaging and distributing the python project . it is used by setup tools to define the configuration of your project 
such as meta data , dependences, and more 
"""
"wherever we have __init__.py file it consider as the package "
""
""
"e. referiing to the setup.py file "

from setuptools import find_packages,setup
from typing import List 

constant='-e.'
def get_requirements()->List[str]:
    "this is function will return list of requirements"

    try:
        requirements=[]
        with open("requirements.txt",'r') as fileobj:
            for line in fileobj.readlines():
                line=line.strip()
                ##ingore empty and -e.
                if line and line !='-e.':
                    requirements.append(line)

                    
                
    except FileNotFoundError:
        print("requirements .txt file not found ")

    return requirements

setup(
    name="Networksecurity",
    version="0.0.1",
    author="Nandhakumar",
    author_email="nandhakumargs8877@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()

)