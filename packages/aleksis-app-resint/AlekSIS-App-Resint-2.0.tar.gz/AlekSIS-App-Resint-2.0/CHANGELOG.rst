Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog`_,
and this project adheres to `Semantic Versioning`_.


`2.0`_ - 2021-12-27
-------------------

Nothing changed.

`2.0b1`_ - 2021-11-07
---------------------

Added
~~~~~

* Provide API view for accessing the current PDF file of a live document (secured with OAuth2).

Changed
~~~~~~~

* German translations were updated.

`2.0b0`_ - 2021-11-03
--------------------

Added
~~~~~

* Provide ``Poster`` model for time-based documents.
  * Organise posters in poster groups.
  * Return current poster of a poster group as PDF file under a specific endpoint.
* Provide ``LiveDocument`` for periodically updated documents.


.. _Keep a Changelog: https://keepachangelog.com/en/1.0.0/
.. _Semantic Versioning: https://semver.org/spec/v2.0.0.html

.. _2.0b0: https://edugit.org/AlekSIS/Official/AlekSIS/-/tags/2.0b0
.. _2.0b1: https://edugit.org/AlekSIS/Official/AlekSIS/-/tags/2.0b1
.. _2.0: https://edugit.org/AlekSIS/Official/AlekSIS/-/tags/2.0
