from setuptools import setup, find_packages

setup(
    name='H2O2_RDE',  # Replace with your project's name
    version='0.1',  # Project version
    packages=find_packages(where='src'),  # Direct setuptools to find your packages
    package_dir={'': 'src'},  # Tell setuptools that packages are under src
    install_requires=[
        'attrs==22.1.0',
        'colorama==0.4.5',
        'cycler==0.11.0',
        'et-xmlfile==1.1.0',
        'fonttools==4.33.3',
        'iniconfig==1.1.1',
        'joblib==1.2.0',
        'kiwisolver==1.4.2',
        'matplotlib==3.5.2',
        'numpy==1.26.1',
        'openpyxl==3.1.2',
        'packaging==21.3',
        'pandas==1.4.2',
        'patsy==0.5.3',
        'Pillow==9.1.0',
        'pluggy==1.0.0',
        'py==1.11.0',
        'pyparsing==3.0.8',
        'pytest==7.1.3',
        'pytest-mock==3.8.2',
        'python-dateutil==2.8.2',
        'pytz==2022.1',
        'scikit-learn==1.1.2',
        'scipy==1.11.3',
        'seaborn==0.12.2',
        'six==1.16.0',
        'sklearn==0.0',
        'statsmodels==0.14.0',
        'threadpoolctl==3.1.0',
        'tomli==2.0.1',
        'typing==3.7.4.3'
    ],

    # Add additional metadata about your project
    author='Ole Golten',
    author_email='ole.golten@nmbu.no',
    description='Tool for analyzing E-chem data from a rotating disk electrode',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # If your README is Markdown
    url='https://github.com/ogo001/H2O2_RDE',  # Project URL
    # More metadata like license, keywords, classifiers etc.
)