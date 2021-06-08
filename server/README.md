# Text adventure API

This is the backend app for the text adventure game.

This project follows a standard structure for Flask apps.

## Installation

1. Run pipenv to install the dependencies:

```bash
pipenv sync
```

1. (Only needs to be done once) Rename `.env.example` file to `.env` file and fill in the settings from your firestore account.
2. Run `pipenv shell` to be inside the virtual environment.
3. To run the testing server, use:

```bash
export FLASK_ENV=development
flask run
```
