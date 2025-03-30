# Manage Airline

A comprehensive Flight Management System built with Python Flask that handles flight scheduling, ticket booking, and airline administration.

## Overview

Manage Airline is a web-based application that provides a complete solution for airline management with different user roles (Admin, Staff, User) and features including flight scheduling, ticket booking, and payment processing.

## Technical Stack

- **Backend**: Python Flask
- **Frontend**: Bootstrap 5
- **Database**: MySQL (SQL Workbench)
- **Authentication**: Built-in auth + Google OAuth

## Features

### Authentication
- User login/signup system
- Google OAuth integration
- Role-based access control (Admin, Staff, User)

### Flight Management
- Flight schedule creation and management
- Flight search functionality
- Flight listing and details

### Ticket System
- Online ticket booking
- Ticket preview
- Form-based ticket creation

### Admin Dashboard
- Flight approval system
- Business rules management
- Statistical reports and analytics

### Payment Integration
- MoMo payment gateway integration
- Secure transaction processing

## Requirements

- Python 3.10 or higher
- MySQL Workbench 8.0.31
- pip (Python package manager)

## Installation

1. Clone the repository
```bash
git clone [repository-url]
cd manage-airline
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure environment variables
   - Create `.env` file in project root
   - Add required configuration:
     ```
     DB_NAME=your_database_name
     DB_PASSWORD=your_database_password
     GOOGLE_CLIENT_ID=your_google_client_id
     GOOGLE_CLIENT_SECRET=your_google_client_secret
     ```

5. Initialize database
   - Ensure MySQL server is running
   - Update database connection details in models.py

6. Run the application
```bash
python index.py
```

## Usage Flow

1. **Staff**: Creates flight schedules
2. **Admin**: Reviews and approves flight schedules
3. **User**: Books tickets for approved flights

## Payment Testing

For testing MoMo payments, download [MOMO UAT Test App](https://developers.momo.vn/v3/vi/docs/payment/onboarding/test-instructions/)

## Development

To set up the development environment in PyCharm:

1. Open project in PyCharm
2. Configure Python Interpreter:
   - Go to File → Settings → Project: manage-airline → Python Interpreter
   - Add Interpreter → Create Virtual Environment
3. Install dependencies in the virtual environment
4. Configure run configuration to execute index.py

## Project Structure

```
manage_airline/
├── static/          # Static assets (CSS, JS)
├── templates/       # HTML templates
│   ├── admin/      # Admin dashboard templates
│   └── layout/     # Base templates and layouts
├── controllers.py   # Route handlers
├── models.py       # Database models
├── dao.py          # Data access objects
└── index.py        # Application entry point
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

---
Happy Flying! ✈️
