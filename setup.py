from setuptools import setup
from profile_cookies import __version__

setup(
    name='browser-profile-cookies',
    version=__version__.version,
    packages=['profile_cookies'],
    python_requires='>=3.9',
    author='C.Kim',
    author_email='yportne8@gmail.com',
    description='Decrypts encrypted cookies from multiple profiles in Chromium browsers on Windows.',
    url='https://github.com/yportne8/profile-cookies',
    install_requires=['pycryptodome>=3.11.0'],
    license='mit'
)