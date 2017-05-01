#!/usr/bin/env python

from setuptools import setup, find_packages

install_requires = [
    'nodeconductor>0.136.1',
    'python-ldap>=2.4.38',
]


setup(
    name='nodeconductor-ldap',
    version='0.1.0.dev0',
    author='OpenNode Team',
    author_email='info@opennodecloud.com',
    url='http://nodeconductor.com',
    description='NodeConductor plugin for structure units management through remote LDAP databases.',
    long_description=open('README.rst').read(),
    package_dir={'': 'src'},
    packages=find_packages('src', exclude=['*.tests', '*.tests.*', 'tests.*', 'tests']),
    install_requires=install_requires,
    zip_safe=False,
    entry_points={
        'nodeconductor_extensions': (
            'nodeconductor_ldap = nodeconductor_ldap.extension:LDAPExtension',
        ),
    },
    include_package_data=True,
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'License :: MIT License',
    ],
)
