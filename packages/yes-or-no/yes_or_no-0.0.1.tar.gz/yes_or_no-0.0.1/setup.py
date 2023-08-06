from setuptools import setup, find_packages


VERSION = '0.0.1'
DESCRIPTION = 'answers yes or no questions'
LONG_DESCRIPTION = '''
                    Should be used in debug string to see if certain
                    conditions are met. Useful in f strings.
                   '''

# Setting up
setup(
    name="yes_or_no",
    version=VERSION,
    author="magedavee (Daniel Davee)",
    author_email="<daniel.v.davee@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'debug'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)