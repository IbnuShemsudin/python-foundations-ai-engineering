
# Student Records Management System

A command-line student management application built with Python.

## Features

- Add, view, search, update, and delete students
- Automatic grade calculation
- Academic performance statistics
- JSON data persistence
- CSV export
- Pandas-powered academic reports
- Input validation and custom exceptions
- Application logging
- Automated unit tests

## Technologies

- Python 3.14
- Pandas
- JSON
- CSV
- Dataclasses
- Unittest

## Setup

Clone the repository and enter the project directory.

Create a virtual environment:

```bash
py -3.14 -m venv .venv
```

Activate it in Git Bash:

```bash
source .venv/Scripts/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run the application

```bash
python -m src.main
```

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Project architecture

- models: Student data model
- services: Business logic
- storage: JSON and CSV persistence
- utils: Validation and exceptions
- reports: Academic reporting
- tests: Automated tests

## Learning objectives

This project demonstrates Python OOP, type hints,
dataclasses, exception handling, file handling,
logging, Pandas, and unit testing.
