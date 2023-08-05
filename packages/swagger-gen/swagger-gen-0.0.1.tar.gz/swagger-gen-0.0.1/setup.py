from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Swagger UI for Flask apps (alpha - in development)'
LONG_DESCRIPTION = 'Automatically generate Swagger UI documentation for a Flask app.  Batteries included.'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="swagger-gen",
    version=VERSION,
    author="Dan Leonard",
    author_email="dcl525@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    package_data={'swagger_gen': ['./resources/swagger.pkl']},
    # include_package_data=True,
    packages=find_packages(),
    install_requires=['flask'],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['python', 'swagger-gen'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
