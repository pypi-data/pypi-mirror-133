import setuptools 

setuptools.setup( 
    name='PyRingD', 
    version='1.1.1', 
    author="Deo Krishna", 
    author_email="deo2k09@gmail.com", 
    description="You can make an alarm clock using this package.",
    long_description="For details, please visit at - 'https://github.com/Deo-Krishna/PyRingD/blob/main/README.md'",  
    packages=["PyRingD"], 
    install_requires=["datetime","playsound","pyttsx3"],  
    classifiers=[ "Programming Language :: Python :: 3", 
    "License :: OSI Approved :: MIT License", 
    "Operating System :: OS Independent", 
    ], 
)