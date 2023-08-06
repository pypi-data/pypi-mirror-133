from setuptools import setup, find_packages


setup(
    name='mosaik-web',
    version='0.4.0',
    author='Stefan Scherfke',
    author_email='mosaik@offis.de',
    description=('A simple simulation visualization for the browser.'),
    long_description=(open('README.rst').read() + '\n\n' +
                      open('CHANGES.txt').read() + '\n\n' +
                      open('AUTHORS.txt').read()),
    url='https://gitlab.com/mosaik/components/data/mosaik-web',
    install_requires=[
        'arrow>=0.4.2',
        'mosaik-api>=3.0',
        'networkx>=2.0',
        'simpy.io>=0.2',
    ],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'mosaik-web = mosaik_web.mosaik:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering',
    ],
)
