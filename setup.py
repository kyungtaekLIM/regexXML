from distutils.core import setup
from regexXML import __version__

setup(
    name='regexXML',
    version=__version__,
    packages=['regexXML',],
    license='Apache 2.0',
    long_description=open('README.md').read(),
)
