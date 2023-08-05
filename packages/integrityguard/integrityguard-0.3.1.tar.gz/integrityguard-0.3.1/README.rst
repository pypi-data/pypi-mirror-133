==============
IntegrityGuard
==============

.. image:: https://img.shields.io/pypi/v/integrityguard.svg
        :target: https://pypi.python.org/pypi/integrityguard

.. image:: https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg
     :target: code_of_conduct.md
     :alt: Contributor Covenant

Multiplatform agent for file integrity monitoring (FIM).

The main motivation for this project is to offer all the minimum features required for a reliable FIM that is independent of any other big monitoring platform.

**IMPORTANT**: This project is currently an ALPHA release. Not suitable for production environment, it is still a work in progress.

Features highlight
--------------------

* Simple and centralized configuration YAML file (``config.yml``)
* Generate logs of any changes in real-time for future auditing
* Push notifications to an API endpoint
* Send email alerts
* Supported hashing methods: "md5", "sha1", "sha224", "sha256", "sha384", "sha512"

How to use it
----------------------

1. To install, run ``pip install integrityguard``
2. Edit the configuration file that will be presented after the installation. (``integrityguard.conf``)
3. Generate the reference hashes, run ``integrityguard --task generate_hashes``
4. Start the monitoring, run ``integrityguard --task monitor``

For more information, run ``integrityguard --help``

Call for contributors
----------------------

This project is just at the begining of its development. We're currently looking for engaged and energized people to colaborate and make it awesome.


