from setuptools import setup, find_packages

VERSION = '0.0.0'
DESCRIPTION = 'Hello there'

# Setting up
setup(
    name="pytca",
    version=VERSION,
    author="Jiri Kovar",
    author_email="jiri@kovar.cz",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy'],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)