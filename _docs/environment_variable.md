#### Birthday Anime API
# Initialize Project
---

This document details the environment variables defined for the operation of the project.

## Document Contents

This document includes:
- **Database Environment Variables:** List of environment variables used for the database.

### Database Environment Variables

- database_motor
Specifies the type of database engine to be used. This variable helps the application understand which database
driver or ORM settings to apply.

**Example**
```ini
  database_motor = "postgresql"
```

- host_port
Specifies the host and port where the database server is running.

**Example**
```ini
  host_port = "127.0.0.1:5432"
```

- name_database
Specifies the name of the database to be used.

**Example**
```ini
  name_database = "name_database"
```

- username_db
Specifies the username for the database connection.

**Example**
```ini
  username_db = "user_database"
```

- password_db
Specifies the password for the database connection.

**Example**
```ini
  password_db = "password_database"
```
