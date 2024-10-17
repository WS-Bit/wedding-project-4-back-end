# Wedding RSVP Backend

This is the backend for a wedding RSVP system built with Django and Django Rest Framework.

## Project Structure

The project consists of the following Django apps:

- `guests`: Handles guest registration and management
- `rsvp`: Manages RSVP submissions
- `songrequests`: Handles song requests from guests
- `memories`: Allows guests to share memories
- `jwt_auth`: Custom JWT authentication

## Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Set up environment variables (see below)
6. Run migrations: `python manage.py migrate`
7. Create a superuser: `python manage.py createsuperuser`
8. Run the development server: `python manage.py runserver`

## Environment Variables

Create a `.env` file in the project root with the following variables:

```
SECRET_KEY=your_secret_key
DEBUG=True
ENVIRONMENT=DEV
DATABASE_URL=your_database_url
SITE_PASSWORD=your_site_password
```

## API Endpoints

- `/api/enter_password/`: Site password verification
- `/api/auth/status/`: Check authentication status
- `/api/guests/`: Guest registration and management
- `/api/rsvp/`: RSVP submission
- `/api/songrequests/`: Song request submission
- `/api/memories/`: Memory sharing and retrieval

## Authentication

The project uses custom JWT authentication. Guests must first enter a site-wide password to access the registration page. After registration, a JWT token is used for subsequent API calls.

## Models

- `Guest`: Stores guest information
- `RSVP`: Manages RSVP responses
- `SongRequest`: Handles song requests
- `Memories`: Stores shared memories

## Testing

Run tests with: `python manage.py test`

## Deployment

The project is configured for deployment on Heroku. Make sure to set the necessary environment variables in your Heroku dashboard.

## Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/YourFeature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin feature/YourFeature`
5. Submit a pull request

## License

This project is licensed under the MIT License.