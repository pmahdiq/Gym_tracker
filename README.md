## About

Gym Tracker is a Django-based web application designed to help users organize their workouts and keep a history of their training sessions.

Users can create training programs, add exercises to them, start a new session from a program, and record the sets, reps, and weight they actually perform.

The project is built to keep each training session independent, so previous workout data is preserved instead of being overwritten.

## Features

- Create and manage training programs
- Add exercises to training programs
- Start training sessions from existing programs
- Record sets, reps, and weight for each exercise
- Keep a history of completed training sessions
- Update and delete training programs
- Track training session duration
- User authentication
- Responsive dark-themed interface

## Tech Stack

- Python
- Django
- PostgreSQL
- HTML
- CSS
- JavaScript
- Git & GitHub

## Project Structure

The project is organized into separate Django applications for account management and workout tracking, with templates and static files handled separately.

## Running the Project

Clone the repository, create a virtual environment, install the dependencies from `requirements.txt`, configure the required environment variables, run the database migrations, and start the Django development server.

```bash
python manage.py migrate
python manage.py runserver
