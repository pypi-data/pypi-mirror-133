from setuptools import setup

setup(
    name='t50metrics',
    version='0.1.0',    
    description='A example Python package',
    url='https://github.com/CAMMA-public/rendezvous',
    author='Chinedu Nwoye',
    author_email='nwoye@unistra.fr',    
    license='BSD 2-clause',
    packages=['t50metrics'],
    install_requires=['scikit-learn',
                      'numpy',
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)    
