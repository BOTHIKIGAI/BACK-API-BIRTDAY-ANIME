# BACK-API-BIRTDAY-ONE-PIECE

The “Happy Birthday One Piece” project is a practical initiative developed in Python 3.12 using the FastAPI framework, with data storage in PostgreSQL 16.
Its purpose is exclusively educational, and for the construction of the backend the best practices of Clean Architecture and Clean Code were applied.

# How to initialize the project?

1. Install python version 3.12
2. Create a virtual environment 
```
python -m venv venv
```
3. Activa virtual environment
- windows
```
venv/Scripts/activate
```
- linux
```
source venv/bin/activate
```
4. Install dependencies
```
pip install -r requirements.txt
```
5. Start project
```
uvicorn main:app --reload
```
# How to create database tables?

## Prerequisites
1. PostgreSQL v16 installed
2. Environment variables configured in the `.env` file with PostgreSQL user and password
3. Create a PostgreSQL database with the name `happy_birthday_anime_db`.

## Command to create the database
1. To be at the root of the project
2. Execute the command
```
python init_db.py
```
3. Verify the creation of tables