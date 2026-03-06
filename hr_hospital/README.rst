===================
Hospital Management
===================

.. |badge1| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
    :target: https://odoo-community.org/page/development-status
    :alt: Beta
.. |badge2| image:: https://img.shields.io/badge/licence-LGPL--3-blue.png
    :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
    :alt: License: LGPL-3
.. |badge3| image:: https://img.shields.io/badge/Odoo-19.0-purple.png
    :target: https://github.com/OCA/server-tools/tree/19.0/hr_hospital
    :alt: Odoo 19.0

|badge1| |badge2| |badge3|

Comprehensive hospital management system for Odoo 19. This module provides complete
functionality for managing doctors, patients, medical visits, diagnoses, schedules,
and generating various medical reports.

**Table of contents**

.. contents::
   :local:

Features
========

Doctor Management
-----------------

* Complete doctor profiles with personal information
* Medical specializations and qualifications
* License tracking and validation
* Intern and mentor system
* Doctor schedules and availability
* Rating system
* Professional experience tracking

Patient Management
------------------

* Comprehensive patient records
* Medical history tracking
* Personal doctor assignment
* Contact person management
* Blood type and allergy tracking
* Visit history with smart buttons
* Quick visit creation

Visit Management
----------------

* Appointment scheduling with validation
* Visit status tracking (Scheduled, Completed, Cancelled, No-show)
* Visit types (Primary, Repeat, Preventive, Unpreventive)
* Cost management
* Doctor recommendations
* Automatic status updates
* Visit rescheduling wizard

Medical Diagnosis
-----------------

* Diagnosis records linked to visits
* Disease database with hierarchical structure
* Treatment prescriptions
* Severity levels (Light, Medium, Heavy, Critical)
* Approval workflow for intern diagnoses
* Disease statistics and reporting

Disease Management
------------------

* Hierarchical disease classification (ICD-10 compatible)
* Disease code tracking (MKX-10)
* Danger levels and contagious status
* Symptom descriptions
* Regional distribution tracking
* Disease report generation

Doctor Schedules
----------------

* Weekly schedule management
* Time slot definition
* Automatic schedule generation wizard
* Conflict detection
* Calendar view integration

Reports & Analytics
-------------------

* Disease statistics with pivot tables
* Graph views (Bar, Line, Pie charts)
* Monthly disease reports
* Doctor performance reports (PDF)
* Visit analytics
* Custom report wizards

Wizards
-------

* **Mass Doctor Reassignment**: Reassign multiple patients from one doctor to another
* **Disease Report**: Generate filtered disease reports by date, doctor, and disease type
* **Visit Rescheduling**: Reschedule visits with conflict detection
* **Schedule Generator**: Auto-generate doctor schedules for specified periods
* **Patient Card Export**: Export patient information with QR codes (if enabled)
* **Monthly Disease Report**: Comprehensive monthly statistics

Security & Access Control
--------------------------

* 5 user roles with hierarchical permissions:

  - **Patient**: View own visits only
  - **Intern**: View and edit own visits
  - **Doctor**: Manage own visits and intern visits
  - **Manager**: View all data, manage schedules
  - **Administrator**: Full access including deletion

* Record rules for data access control
* Field-level security
* Role-based menu visibility

Installation
============

Requirements
------------

* Odoo 19.0 Community or Enterprise
* PostgreSQL 12 or later
* Python 3.10 or later

Installation Steps
------------------

1. Download the module and place it in your Odoo addons directory::

    cd /path/to/odoo/addons
    git clone https://github.com/yourname/hr_hospital.git

2. Update the apps list::

    Settings → Apps → Update Apps List

3. Search for "Hospital Management" and click Install

4. (Optional) Install with demo data to see sample records

Configuration
=============

User Roles
----------

After installation, assign user roles:

1. Go to ``Settings → Users & Companies → Users``
2. Select a user
3. Go to ``Access Rights`` tab
4. Under ``Hospital Management``, select appropriate role:

   * Patient (basic access)
   * Intern (medical student)
   * Doctor (licensed physician)
   * Manager (administrative)
   * Administrator (full control)

Initial Setup
-------------

1. **Create Specializations**:

   * Go to ``Hospital → Configuration → Specializations``
   * Add medical specializations (e.g., Cardiology, Pediatrics)

2. **Add Doctors**:

   * Go to ``Hospital → Doctors``
   * Create doctor profiles with specializations
   * For interns, assign mentors

3. **Register Patients**:

   * Go to ``Hospital → Patients``
   * Add patient information
   * Assign personal doctors

4. **Create Schedules**:

   * Go to ``Hospital → Schedules``
   * Use Schedule Generator wizard for bulk creation
   * Or create individual schedule entries

Usage
=====

Scheduling a Visit
------------------

**Method 1: From Patient Card**

1. Open patient record
2. Click "Create Visit" button
3. Select date and doctor
4. Save

**Method 2: From Visits Menu**

1. Go to ``Hospital → Visits``
2. Click Create
3. Select patient and doctor
4. Set scheduled date/time
5. Save

Creating a Diagnosis
--------------------

1. Open a completed visit
2. Create new diagnosis record
3. Select disease from database
4. Enter treatment and severity
5. If you're an intern, diagnosis requires approval

Generating Reports
------------------

**Disease Statistics**

1. Go to ``Hospital → Reports → Disease Statistics``
2. Use pivot view for custom analysis
3. Switch to graph view for visualizations
4. Apply filters as needed

**Doctor Report (PDF)**

1. Open doctor record
2. Click ``Print → Doctor Report``
3. PDF includes visit history and patient list

**Monthly Disease Report**

1. Go to ``Hospital → Reports → Monthly Disease Report``
2. Select month and filters
3. Click "Generate Report"
4. View results in list/graph/pivot views

Known Issues / Roadmap
======================

Known Issues
------------

* Large datasets (>10,000 patients) may experience slow pivot view loading
* PDF report generation may timeout with >1000 visits

Planned Features
----------------

* Integration with external laboratory systems
* SMS/Email appointment reminders
* Patient portal for self-service
* Medical imaging integration
* Prescription printing
* Insurance claim management
* Telemedicine support

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/EvgenyNorb/hr_hospital/issues>`_.

In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed
`feedback <https://github.com/EvgenyNorb/MyOdoo19Test/tree/19.0>`_.

Credits
=======

Authors
-------

* Your Company Name

Contributors
------------

* Your Name <Evgeny.norb@gmail.com>

Maintainers
-----------

This module is maintained by Your Company.

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

This module is part of the `OCA/server-tools <https://github.com/OCA/server-tools/tree/19.0/hr_hospital>`_ project on GitHub.

You are welcome to contribute. To learn how, please visit https://odoo-community.org/page/Contribute.