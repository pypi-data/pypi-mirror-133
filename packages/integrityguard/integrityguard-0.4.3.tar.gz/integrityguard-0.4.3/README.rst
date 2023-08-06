==============
IntegrityGuard
==============

.. image:: https://img.shields.io/pypi/v/integrityguard?label=PyPI
     :target: https://pypi.python.org/pypi/integrityguard
     :alt: PyPI current version

.. image:: https://img.shields.io/pypi/dm/integrityguard?label=Downloads
     :target: https://pypi.python.org/pypi/integrityguard
     :alt: PyPI downloads

.. image:: https://img.shields.io/pypi/pyversions/integrityguard?label=Python
     :target: https://pypi.python.org/pypi/integrityguard
     :alt: Python

.. image:: https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg
     :target: code_of_conduct.md
     :alt: Contributor covenant

Multiplatform agent for file integrity monitoring (FIM).

The main motivation for this project is to offer all the minimum features required for a reliable FIM that is independent of any other big monitoring platform.

**IMPORTANT**: This project is currently an ALPHA release. Not suitable for production environment, it is still a work in progress.

Features highlight
--------------------

* Simple and centralized configuration file (``integrityguard.conf``)
* Generate logs of any changes in real-time for future auditing
* Push notifications to an API endpoint
* Send email alerts
* Supported hashing methods: "md5", "sha1", "sha224", "sha256", "sha384", "sha512"

How to use it
----------------------

1. To install, run ``pip install integrityguard``
2. Edit/provide the configuration file (``integrityguard.conf``)

   - To copy the original .conf file, run ``integrityguard --task copy_config --destination <full_path>``
   - To provide the new .conf file path use ``--config <full_path>``

3. Generate the reference hashes, run ``integrityguard --task generate_hashes``

   - To provide the target path via command, run ``integrityguard --task generate_hashes --target <full_path>``

4. Start the monitoring, run ``integrityguard --task monitor``

   - To provide the target path via command, run ``integrityguard --task monitor --target <full_path>``

**IMPORTANT**: By providing configurations via command line anything defined via .conf file will be overwritten.

For more information, run ``integrityguard --help``

Call for contributors
----------------------

This project is just at the begining of its development. We're currently looking for engaged and energized people to colaborate and make it awesome.


