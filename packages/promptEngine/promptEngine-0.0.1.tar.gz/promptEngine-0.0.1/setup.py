from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Helps create prompts!'
LONG_DESCRIPTION = 'Helps create choice boxes and prompts within the GUI.'

# Setting up
setup(
        name="promptEngine", 
        version=VERSION,
        author="Ishan Ajay",
        author_email="ishanajay@thetechmaker.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['tk', 'Pillow'], 
        setup_requires=['wheel'],

        keywords=['python', 'first package', 'prompt', 'gui', 'promptEngine'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)