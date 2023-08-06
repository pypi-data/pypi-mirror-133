from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Adversarial ML Library'
LONG_DESCRIPTION = 'A library implementing adversarial ML algorithms'

# Setting up
setup(
        name="adverseml", 
        version=VERSION,
        author="TRIPODS",
        author_email="tsivap2@uic.edu",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that needs to be installed along with your package
        
        keywords=['python', 'adversarial', 'machine learning', 'lipschitz partition'],
        
        classifiers= [ 
        # as given in https://pypi.org/classifiers/
            "Development Status :: 2 - Pre-Alpha",
            "Intended Audience :: Science/Research",
            "Intended Audience :: Developers",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: POSIX :: Linux",
        ]
)
