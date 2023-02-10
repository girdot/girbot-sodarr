from setuptools import setup

setup(
    name='girbot-sodarr',
    version='0.1.0',    
    description='A radarr/sonarr plugin for modular discord bot girbot',
    url='https://github.com/girdot/girbot-sodarr',
    author='Danial Cauley',
    author_email='girdot@gmail.com',
    license='MIT',
    packages=['girbot-sodarr'],
    install_requires=['requests>=2.28.2'],
    classifiers=[],
)
