from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'django-knox-for'
LONG_DESCRIPTION = 'django-knox-for from Django >= 4'

# Setting up
setup(
    name="django-knox-for",
    version=VERSION,
    author="Tordoir Julien",
    author_email="<jt.tordoir@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['django', 'djangorestframework', 'django-knox-for'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)