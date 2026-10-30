.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

===========
Sale Sintra
===========

Group sale orders under Sintras: objectives with the data of the installation,
the IB data and their own status.

Key features
============

* **Sintra** menu, under *Sales > Orders* and as its own application. Each
  Sintra has:

  * Objective (unique), status, customer, project, registration, work,
    installation code, installation, features, cabinet purchase order,
    delivery date, planned date and note.
  * Region, zone and UTD.
  * IB data: IB delivery date, installer, IB manager and SIM.
  * **Sales Orders** tab with its sale orders.
  * **Documentation** tab: file name, server folder and note of each document.

* The status (Draft, Pending Sales, Unplanned, Planned, Tested, Sent,
  Received, Cancelled) is changed by clicking on it.
* **Send Email to Sales** button: emails the Sintra objective and installation
  to the users that receive the Sintra notice to Sales, logs it in the chatter,
  marks the Sintra as *Email Sent to Sales* and sets it to *Pending Sales*.
* On sale orders:

  * **Sintra** field, and a **Sintra** tab with the Sintra data when it is set.
  * **Sintra** column in the quotations and sales orders lists.
  * **Assign to Sintra** action in those lists, to assign the selected orders
    to a Sintra.

* On sale order lines: **IB Code** column and optional columns with the Sintra
  data of the order.

Configuration
=============

* **Sintra / User**: sees the Sintras and the Sintra fields of sale orders.
* **Sintra / Manager**: also creates and edits Sintras and assigns sale orders
  to them.
* **Sintra Notice to Sales / Receive Sintra Notice to Sales**: receives the
  email sent to Sales from a Sintra.

The Sintra groups give read access to sale orders. To assign sale orders to a
Sintra, users also need write access to sale orders.

Usage / How to test
===================

1. Create a Sintra in **Sintra** and fill in its data.
2. Select some quotations or sales orders in their list and use
   **Action > Assign to Sintra**.
3. Open one of those orders: the **Sintra** tab shows the Sintra data.
4. Add a user to *Receive Sintra Notice to Sales* and click
   **Send Email to Sales** on the Sintra.

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

* Lucía Echeverría <luciaecheverria@avanzosc.es>
* Ana Juaristi <anajuaristi@avanzosc.es>
