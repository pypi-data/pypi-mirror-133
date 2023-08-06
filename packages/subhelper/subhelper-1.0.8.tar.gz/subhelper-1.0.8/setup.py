from setuptools import setup, find_packages

__licence__ = 'GPLv3+'
__author__ = 'Nabil-Fareed Alikhan'
__author_email__ = 'nabil@happykhan.com'
__version__ = "1.0.8"


min_version = (3, 9)

with open(file="README.md", mode="r") as readme_handle:
    long_description = readme_handle.read()

setup(
    
    name='subhelper',
    author=__author__,
    author_email=__author_email__,
    version=__version__,
    description='Helper scripts for submission to ena (microbial + sarscov2) and gisaid (sarscov2 only)',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/happykhan/subhelper',
    project_urls = {
        "Source": "https://github.com/happykhan/subhelper",
    },    
    tests_require='nose',
    install_requires=[
        'biopython', 
        'marshmallow', 
        'numpy', 
        'pyaml', 
        'PyYAML', 
        'requests', 
        'openpyxl',
        'wheel'
        ],
    keywords='gisaid, microbial, genomics, ena, data, submission',
    packages=find_packages(),
    include_package_data=True,
    python_requires = '>={}'.format('.'.join(str(n) for n in min_version)),
    extras_require = {},
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',    
        "Programming Language :: Python :: 3.9",    
        "Programming Language :: Python :: 3.10",            
    ],
    entry_points={
        'console_scripts': ['enahelper=enahelper.enasub:cli', 'gisaidhelper=gisaidhelper.gisaidsub:cli']
    }    
)