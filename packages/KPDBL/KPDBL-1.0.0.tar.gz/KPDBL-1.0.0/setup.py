from setuptools import setup, find_packages, find_namespace_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License'
]

setup(
    name='KPDBL',
    version='1.0.0',
    description='A simple and fast key value database',
    long_description=open('README.md').read() + '\n\n' +
    open('CHANGELOG.md').read(),
    long_description_content_type="text/markdown",
    url='https://www.github.com/sarangt123/kpdbl-database',
    author='Sarang T (github.com/sarangt123)',
    author_email='sarang.thekkedathpr@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='Augmented reality',
    install_requires=[],
    packages=find_packages(),
    python_requires=">=3.6"

)
