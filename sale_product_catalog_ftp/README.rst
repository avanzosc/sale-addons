.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

==================================
Sale Product Catalog Upload to FTP
==================================

This module extends ``sale_product_catalog`` to automatically generate the
product catalog XLSX report for a given customer and upload it to that
customer's FTP server.

It only uses the Python standard library (``ftplib``), so no external
dependency is needed.

Key features
============

* New model ``product.catalog.ftp`` that pairs a **product catalog** with a
  **customer** (unique per catalog/customer), storing the FTP connection
  settings: host, login, password (masked in the UI), timeout (default 30
  seconds) and destination folder.
* Generation of the catalog XLSX report (the one provided by
  ``sale_product_catalog`` for the customer's pricelist) and upload to the
  FTP server with the ``STOR`` command.
* **Daily cron** that regenerates and uploads all the configured catalogs
  (runs every day at 01:00).
* Manual **Upload** server action available from the list view for selected
  records.
* **Error handling**: any connection or upload error is stored in the
  ``ftp_error`` field, shown in red in the list view, and a filter
  (*Errored*) is available in the search view.
* Local files are stored under ``~/<base folder>/<partner id>/<catalog id>/``,
  where the base folder is defined by the system parameter
  ``product_catalog_ftp.base_ftp_folder`` (default: ``ftp_catalog``).
* When a configuration is archived, its customer or catalog is changed, or
  the record is deleted, the generated file is removed from both the local
  folder and the FTP server.
* **Multi-company** — a record rule ensures users only see the upload
  configurations of catalogs belonging to their allowed companies.
* Access rights: read access for all internal users; full management
  restricted to administrators (Settings group).

Usage
=====

1. Go to **Sales → Products → Catalogs → Upload Catalog to FTP**.
2. Create one line per customer and catalog, filling in the FTP host, login,
   password, and destination folder.
3. Select the records and run the **Upload** action from the list view, or
   wait for the daily cron to generate and upload the catalogs.
4. Check the **FTP Error** column (or the *Errored* filter) to detect failed
   uploads.
5. On the catalog form, the **Upload to FTP** page shows the customers with
   an upload configuration for that catalog.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/avanzosc/sale-addons/issues>`_. In case of trouble,
please check there if your issue has already been reported. If you spotted
it first, help us smash it by providing detailed and welcomed feedback.

Do not contact contributors directly about support or help with technical
issues.

Credits
=======

Contributors
------------

* Oihane Crucelaegui <oihanecrucelaegui@avanzosc.es>
