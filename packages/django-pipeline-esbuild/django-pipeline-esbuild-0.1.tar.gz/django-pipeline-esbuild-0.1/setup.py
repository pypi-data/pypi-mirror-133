# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


description = """
Django pipeline compiler plugin that uses esbuild
"""

setup(
    name='django-pipeline-esbuild',
    version='0.1',
    # use_scm_version={"version_scheme": "post-release"},
    setup_requires=["setuptools_scm"],
    description=description,
    long_description=description,
    author='Essau Ramirez',
    author_email='essau@three-dimensional.space',
    url='https://github.com/sauramirez/django-pipeline-esbuild',
    license='MIT',
    packages=find_packages(exclude=['tests', 'tests.tests']),
    zip_safe=False,
    include_package_data=True,
    keywords=('django pipeline esbuild plugin'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ]
)
