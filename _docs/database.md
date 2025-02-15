#### Birthday Anime API
# Database Configuration
---

This document describes the processes for initializing the database, detailing the steps necessary to create
the database.

## Document Contents

This document includes:
- **Prerequisites:** List of tools, versions and dependencies needed.
- **Create Database:** Steps to create the database.
- **Create Tables:** Steps to create the tables.

### Prerequisites
- psql (PostgreSQL) 17.x

### Create Database
1. Access PostgreSQL prompt as postgres user
```bash
sudo -u postgres psql
```
2. Create database
```sql
CREATE DATABASE database_name;
```
3. Verify database creation
```sql
\l
```
4. Connect to the database
```sql
\c database_name
```
6. Exit PostgreSQL prompt
```sql
\q
```
### Create Tables
1. Execute the command in the root of the project
```shell
python init_db.py
```
