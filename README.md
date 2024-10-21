This repository provides an authentication service using Django Rest Framework (DRF) with Google OAuth2. It allows users to authenticate using their Google accounts, simplifying the login process and enhancing security.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Google API Setup](#google-api-setup)
- [App Configuration](#app-configuration)
- [Testing](#testing)

## Prerequisites

Before you begin, ensure you have the following software installed:

- Python 3.12 or higher
- Poetry
- Docker and Docker Compose

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your_username/drf_google_oauth2.git
   cd drf_google_oauth2

2. Install the dependencies:

## Google API Setup

1. Reach out to the google cloud website and create a new project, then get the project's API Client and API Secret to use in your .env file.
_You can copy the structure from .env.example file__

2. Add your callback url to your google cloud project
```http://localhost:8000/auth/google/callback/```

## App Configuration

1. Activate your virtual environment
2. Run poetry install
3. Run pre-commit install
4. Setup your .env file based on .env.example
5. Run python manage.py migrate
6. Run python manage.py runserver

Now you should have a server up and running that serves jwt!

just go to:
https://accounts.google.com/o/oauth2/v2/auth?client_id=<CLIENT_ID>&redirect_uri=http://localhost:8000/auth/google/callback/&response_type=code&scope=email%20profile

and after running the steps you should get an access and refresh token.

## Testing
Run python manage.py test
