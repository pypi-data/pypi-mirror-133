from setux.core.mapping import Packages


class Fedora(Packages):
    pkg = dict(
        netcat = 'nmap-ncat',
    )


class Arch(Packages):
    pkg = dict(
        setuptools = 'python-setuptools',
        pip        = 'python-pip',
        netcat     = 'openbsd-netcat',
        sqlite     = 'sqlite3',
    )


class Fedora(Packages):
    pkg = dict(
        setuptools = 'python3-setuptools',
        pip        = 'python3-pip',
        netcat     = 'nmap-ncat',
    )


class Artix(Packages):
    pkg = dict(
        setuptools = 'python-setuptools',
        pip        = 'python-pip',
        netcat     = 'openbsd-netcat',
        sqlite     = 'sqlite3',
        cron       = 'cronie',
    )
