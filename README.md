# CountyConnect — Public Service Request System

CountyConnect is a Django-based web application inspired by Kenya's eCitizen platform. It aims to make county public services more accessible by allowing citizens to browse services, submit requests, track progress, and receive updates.

The system provides a central platform for citizens and county staff to manage public service requests in an organized and transparent way.

## Table of Contents

- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [County Service Categories](#county-service-categories)
- [Administrative Features](#administrative-features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation and Setup](#installation-and-setup)
- [Environment Configuration](#environment-configuration)
- [Database Design](#database-design)
- [Application URLs](#application-urls)
- [Request Status Workflow](#request-status-workflow)
- [Testing Checklist](#testing-checklist)
- [Development Guide](#development-guide)
- [Security Considerations](#security-considerations)
- [Future Improvements](#future-improvements)

## Project Overview

CountyConnect is designed to support digital delivery of county services in Kenya. It provides citizens with a convenient way to interact with county departments without having to rely entirely on manual paperwork or physical visits.

The application is intended to support:

- Citizen registration and account management.
- Online access to county departments and service listings.
- Submission and tracking of public service requests.
- Request processing and status management by authorized staff.
- Email notifications about relevant request updates.
- Centralized management of services and service requests.

## Key Features

### Citizen Features

- Create an account and log in securely.
- Browse available county departments and services.
- View service descriptions, requirements, and applicable fees.
- Submit public service requests.
- View previously submitted requests.
- Track request status and progress.
- Filter requests by status.
- View individual request details.
- Receive email notifications when supported by the application configuration.

### Staff Features

- Access request-management functionality based on staff permissions.
- View and manage service requests.
- Update request statuses.
- Review request information and follow up on pending cases.
- Communicate progress through the request workflow.

### Service Management

- Organize services by county department.
- Maintain service descriptions and requirements.
- Display applicable fees in Kenyan shillings (KES).
- Enable or disable service listings.
- Keep service information organized for citizens.

## County Service Categories

The system can organize public services under categories such as the following. Actual availability depends on the services configured in the database.

| Department | Example Services |
|---|---|
| Health Services | Public health inspections, health facility enquiries, sanitation complaints |
| Land and Physical Planning | Land-use enquiries, development approvals, building-plan applications |
| Public Works | Public facility maintenance, drainage complaints, infrastructure requests |
| Revenue and Licensing | Business permit applications, license renewals, county fee enquiries |
| Roads and Transport | Road damage reports, traffic signage requests, transport-related enquiries |
| Water and Sanitation | Water supply complaints, water outage reports, drainage and sanitation issues |

Departments and services should be configurable so the system can adapt to different county needs.

## Administrative Features

The administrative area is intended to support authorized county personnel in managing the platform.

Potential administrative responsibilities include:

- **Department management:** Create, update, activate, or deactivate departments.
- **Service management:** Maintain service descriptions, requirements, and fees.
- **Request management:** Review submitted requests and update their statuses.
- **User management:** Manage accounts and staff permissions.
- **Access control:** Restrict administrative operations to authorized users.
- **Request monitoring:** Review pending, in-progress, and resolved requests.
- **Data maintenance:** Keep service and department information accurate.

Only include features in this section as implemented functionality when they have been built and tested. Django's built-in admin site may provide some administrative capabilities without a custom dashboard.

## Technology Stack

- **Backend:** Python and Django
- **Database:** PostgreSQL
- **Frontend:** HTML, CSS, Bootstrap and Django templates
- **Authentication:** Django authentication system
- **Email:** Django email backend with SMTP configuration
- **Version Control:** Git and GitHub

## Project Structure

The following is a guide to the main files and directories. Your exact project may contain additional files or different app names.

```text
county_ecitizen/
├── accounts/
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── services/
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── templates/
│   ├── services/
│   └── ...
├── static/
│   └── css/
│       └── style.css
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

### Main Components

- `accounts/`: User account and authentication functionality.
- `config/`: Django project configuration and root URL routing.
- `services/`: County service listings, request submission, tracking, and staff request management.
- `templates/`: HTML templates rendered by Django.
- `static/`: CSS, JavaScript, and other static assets.
- `manage.py`: Command-line utility for Django administration.
- `requirements.txt`: Python package dependencies.
- `.env.example`: Example environment configuration without real credentials.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/mandy-lazer/countyconnect.git
cd countyconnect
```

### 2. Create a virtual environment

Linux and macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows:

```powershell
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a local `.env` file if your project uses a library such as `python-dotenv` or `django-environ`. Otherwise, configure the required environment variables through your shell or deployment platform.

Use `.env.example` as a template. Never commit real credentials.

### 5. Configure PostgreSQL

Create a PostgreSQL database and a database user with appropriate permissions. Configure Django to connect using the values specified in your environment.

Example database settings:

```text
DB_NAME=countyconnect
DB_USER=countyconnect_user
DB_PASSWORD=replace_with_your_local_password
DB_HOST=localhost
DB_PORT=5432
```

These are example variable names. Your `settings.py` must explicitly read them for this configuration to work.

### 6. Apply database migrations

```bash
python manage.py migrate
```

### 7. Create an administrator account

```bash
python manage.py createsuperuser
```

Follow the prompts to create the account.

### 8. Start the development server

```bash
python manage.py runserver
```

Open the local address:

`http://127.0.0.1:8000/`

The exact landing page and available routes depend on your root URL configuration.

## Environment Configuration

Configuration should be supplied through environment variables rather than hardcoded production values.

Common settings include:

| Variable | Purpose |
|---|---|
| `SECRET_KEY` | Django cryptographic signing key |
| `DEBUG` | Enables or disables Django debug mode |
| `ALLOWED_HOSTS` | Hosts permitted to serve the application |
| `DB_NAME` | PostgreSQL database name |
| `DB_USER` | Database username |
| `DB_PASSWORD` | Database password |
| `DB_HOST` | Database server hostname |
| `DB_PORT` | Database server port |
| `EMAIL_HOST` | SMTP server hostname |
| `EMAIL_PORT` | SMTP server port |
| `EMAIL_HOST_USER` | SMTP account username |
| `EMAIL_HOST_PASSWORD` | SMTP credential or app password |
| `EMAIL_USE_TLS` | Enables SMTP TLS where configured |

Variable names must match the implementation in `config/settings.py`. The `.env` file should remain local and must be excluded from Git.

## Database Design

The application uses Django models backed by PostgreSQL. The exact schema is defined by the models and migrations in the repository.

### Core Entities

**User / Citizen**

Represents a person using the platform. Django authentication can provide login credentials and user permissions.

**Department**

Represents a county department responsible for one or more public services. Department information can include its name, description, contact email, and active status.

**Service**

Represents a service offered by a department. Typical fields include its name, department, description, requirements, fee in KES, and active status.

**ServiceRequest**

Represents a citizen's request for a county service. It links a citizen to a service and stores information such as the request details, status, and timestamps, depending on the implemented model.

### Relationship Overview

```text
User / Citizen
      |
      | submits
      v
ServiceRequest ---------> Service
                              |
                              | belongs to
                              v
                         Department
```

A department can offer multiple services. A service can receive multiple requests, and a citizen can submit multiple requests.

Refer to `models.py` and the migrations for the authoritative database schema.

## Application URLs

The following table describes typical application routes. Confirm the exact paths and URL names in `config/urls.py`, `accounts/urls.py`, and `services/urls.py` before treating this table as the definitive route map.

| Page or Function | Purpose |
|---|---|
| `/` | Application landing page, if configured |
| `/admin/` | Django administration site |
| `/accounts/` | Account-related routes, if grouped under this prefix |
| `/services/` | Service-related routes, if grouped under this prefix |
| `/services/submit/` | Example service-request submission route |
| `/services/my-requests/` | Example citizen request list |
| `/services/track/` | Example request-tracking route |
| `/services/requests/<id>/` | Example request details route |

These are illustrative paths, not a verified list of the repository's current URL patterns. The actual paths may differ.

To inspect the configured routes, review the project's URL configuration files or use an installed URL-inspection tool.

## Request Status Workflow

A request workflow helps citizens and staff understand the progress of each case.

A typical workflow is:

```text
Pending
   |
   v
In Progress
   |
   v
Resolved
```

Depending on the implementation, a request may also be rejected, cancelled, or reopened. Those states should only be documented as available if they are present in the model and supported by the application logic.

### Status Definitions

- **Pending:** The request has been submitted and is awaiting review.
- **In Progress:** An authorized staff member is handling the request.
- **Resolved:** The request has been completed according to the service process.

### Expected Workflow

1. A citizen selects an available service and submits a request.
2. The system records the request and assigns its initial status.
3. Authorized staff review the request.
4. Staff update the status as work progresses.
5. The citizen views the updated status in their request list or detail page.
6. Email notifications may be sent if the relevant notification logic is configured.

Access controls should ensure that citizens can view only their own requests and that only authorized staff can change request statuses.

## Testing Checklist

Before releasing a version, test the following scenarios.

### Authentication and Accounts

- [ ] Users can register and log in where registration is implemented.
- [ ] Invalid login credentials are rejected.
- [ ] Anonymous users cannot access protected pages.
- [ ] Logout works correctly.
- [ ] Staff-only pages reject unauthorized users.

### Departments and Services

- [ ] Active departments are displayed correctly.
- [ ] Active services appear under the correct department.
- [ ] Inactive services cannot be submitted through the request form.
- [ ] Service descriptions, requirements, and fees display correctly.
- [ ] Empty service listings are handled gracefully.

### Service Requests

- [ ] A citizen can submit a valid request.
- [ ] Invalid form data is rejected with useful validation messages.
- [ ] A submitted request is associated with the correct citizen and service.
- [ ] Citizens can view their own requests.
- [ ] Citizens cannot access another citizen's private request details.
- [ ] Status filters return the correct requests.
- [ ] Only authorized staff can update request statuses.
- [ ] Email notifications work when enabled and configured.

### Database and Operations

- [ ] Migrations apply successfully to a fresh database.
- [ ] Application behavior is correct with PostgreSQL.
- [ ] Database connection errors are handled safely.
- [ ] Static files are collected and served correctly in deployment.
- [ ] The application starts without Django system-check errors.

### Security

- [ ] Secrets are not committed to Git.
- [ ] Production mode uses `DEBUG=False`.
- [ ] `ALLOWED_HOSTS` is configured correctly.
- [ ] HTTPS is enforced in production.
- [ ] CSRF protection remains enabled for forms.
- [ ] User permissions are checked server-side.
- [ ] Error pages do not expose stack traces or sensitive configuration.

## Development Guide

### Common Django Commands

Run database migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

Create an administrator account:

```bash
python manage.py createsuperuser
```

Run automated tests:

```bash
python manage.py test
```

Check the project configuration:

```bash
python manage.py check
```

Collect static files for deployment:

```bash
python manage.py collectstatic
```

### Development Practices

- Use Git branches for substantial new features.
- Keep dependencies documented in `requirements.txt`.
- Create migrations whenever model changes require them.
- Write automated tests for authentication, permissions, request creation, and status updates.
- Keep development, testing, and production settings appropriately separated.
- Review logs and test error handling before deploying.
- Document changes that affect database models, routes, or environment variables.

## Security Considerations

CountyConnect may process personal information and public-service request details, so security should be considered throughout development.

- Store passwords using Django's authentication framework; never store plaintext passwords.
- Keep Django secret keys, database credentials, SMTP passwords, and API tokens out of source control.
- Use environment variables or a secure secrets manager for deployment configuration.
- Set `DEBUG=False` in production.
- Configure `ALLOWED_HOSTS` and HTTPS appropriately.
- Use Django's CSRF protection and server-side validation.
- Enforce authorization checks in views, not just in templates.
- Ensure citizens can access only their own request records.
- Restrict staff and administrative actions to authorized accounts.
- Use least-privilege database credentials.
- Keep dependencies updated and review security advisories.
- Avoid logging passwords, tokens, or sensitive personal information.
- Back up the database and define an appropriate recovery process.
- Collect and retain only information necessary for the service.
- Follow applicable Kenyan data protection requirements when handling personal information.

## Future Improvements

Potential future enhancements include:

- SMS notifications for request updates.
- M-Pesa integration for services that require payment.
- Uploads for supporting documents.
- More detailed staff roles and departmental permissions.
- Request assignment to specific staff members.
- Search, filtering, and reporting dashboards.
- Service-level targets and overdue-request alerts.
- Citizen feedback and satisfaction ratings.
- Audit logs for administrative actions.
- API endpoints for approved integrations.
- Automated deployment and continuous integration.
- Accessibility and mobile usability improvements.

## Contribution

Contributions and suggestions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Make your changes and add tests.
4. Run the test suite.
5. Submit a pull request describing the changes.

## License

Add a license before distributing the project for reuse. Until a license is included, do not assume that others have permission to reuse, modify, or redistribute the source code.

## Author

**Mandy Lazer**

GitHub: https://github.com/mandy-lazer
