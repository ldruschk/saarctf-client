from distutils.core import setup

setup(
    name='saarctf_client',
    version='0.1',
    description='Python library to develop exploits with the saarCTF status API',
    packages=['saarctf_client'],
    install_requires=[
        'requests',
        'requests-cache',
        'redis'
    ],
)
