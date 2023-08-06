from sys import version_info, platform
from setuptools import setup

requirements = [
    'aiosqlite==0.17.0',
    'telethon==1.24.0',
    'ecdsa==0.16.1',
    'filetype==1.0.8',
    'cryptg==0.2.post2',
    'pycryptodome==3.10.1',
    'sphinx-rtd-theme==1.0.0', 
    'regex==2021.11.10'
]
if version_info > (3, 7) and platform not in ('win32', 'cygwin', 'cli'):
    requirements.append('uvloop==0.16.0')

setup(
    name             = 'tgbox',
    packages         = ['tgbox'],
    version          = '0.3.2',
    license          = 'LGPL-2.1',
    description      = 'Encrypted cloud storage based on Telegram API',
    author           = 'NonProjects',
    url              = 'https://github.com/NonProjects/tgbox',
    download_url     = 'https://github.com/NonProjects/tgbox/archive/refs/tags/indev%230.3.2.tar.gz',

    package_data = {
        'tgbox': ['tgbox/other'],
    },
    include_package_data = True,
    install_requires = requirements,

    keywords = [
        'Telegram', 'Cloud-Storage', 
        'API', 'Asyncio', 'Non-official'
    ],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Security :: Cryptography',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Archiving :: Backup',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ]
)
