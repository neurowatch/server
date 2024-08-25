# Neurowatch Server

Server code for the neurowatch project.

This includes the backend and frontend templates.

# Setup

Execute the migrations, the 0001 migration file should be available, if not, execute ``python manage.py makemigrations`.

Create an user using `python manage.py createsuperuser`

Run the server and log into the admin panel and create a token, this token will be used by the clients to authenticate.

At this point the system should be ready to be used.
