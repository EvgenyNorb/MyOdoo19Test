=========
Changelog
=========

..
    Changelog entries should follow this format:

    Version Number (YYYY-MM-DD)
    ---------------------------

    **Features**
    - Description of new feature

    **Improvements**
    - Description of improvement

    **Bugfixes**
    - Description of bugfix

    **Technical**
    - Technical changes


19.0.1.0.0 (2026-03-06)
-----------------------

**Initial Release**

This is the first stable release of the Hospital Management module for Odoo 19.

**Features**

- Complete doctor management system with personal profiles
- Intern and mentor relationship tracking
- Patient records with medical history
- Visit scheduling and management system
- Medical diagnosis with disease database
- Hierarchical disease classification (parent-child relationships)
- Doctor schedule management with calendar view
- Patient doctor history tracking
- Contact person management for patients
- Security groups with 5 role levels (Patient, Intern, Doctor, Manager, Admin)
- Record rules for data access control
- Smart buttons for quick navigation
- Kanban views for doctors and visits
- Pivot and graph views for analytics

**Wizards**

- Mass Doctor Reassignment Wizard
- Disease Report Wizard with advanced filtering
- Visit Rescheduling Wizard
- Doctor Schedule Generator Wizard
- Patient Card Export Wizard
- Monthly Disease Report Wizard

**Reports**

- Doctor Report (PDF) with visit history and patient list
- Disease Statistics with pivot tables
- Graph visualizations (bar, line, pie charts)
- Monthly disease analytics

**Views**

- List/Tree views with advanced search and filters
- Kanban views with drag-and-drop support
- Form views with smart buttons and computed fields
- Pivot views for data analysis
- Graph views for visual analytics
- Calendar views for schedules

**Technical**

- Odoo 19.0 compatible
- Python 3.10+ support
- PostgreSQL optimized queries
- Proper indexing on key fields
- Computed fields with store=True for performance
- Validation constraints for data integrity
- Onchange methods for UX improvements
- Unit tests covering core functionality
- Demo data for testing and demonstration

**Security**

- Group-based access control
- Record rules for row-level security
- Field-level access restrictions
- Hierarchical group inheritance
- Password-protected sensitive data

**Localization**

- Translatable fields (name, description, symptoms)
- Multi-language support ready
- Date/time formatting based on user locale


19.0.0.1.0 (2026-02-15) - Beta
------------------------------

**Features**

- Basic doctor and patient models
- Simple visit management
- Initial security groups

**Known Issues**

- Performance issues with large datasets (fixed in 1.0.0)
- Missing validation on intern without mentor (fixed in 1.0.0)


Future Roadmap
==============

19.0.2.0.0 (Planned)
--------------------

**Planned Features**

- Integration with external laboratory systems
- SMS and Email appointment reminders
- Patient self-service portal
- Medical imaging attachment support
- Electronic prescription printing
- Insurance claim management
- Telemedicine consultation support
- Mobile app for doctors

**Planned Improvements**

- Performance optimization for large datasets
- Enhanced reporting with custom templates
- Advanced search with full-text indexing
- Batch operations for administrative tasks
- API endpoints for third-party integration

**Planned Technical Changes**

- Migration to new ORM features in Odoo 19
- Improved caching strategies
- Database query optimization
- Asynchronous task processing for reports