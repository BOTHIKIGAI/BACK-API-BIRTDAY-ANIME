#### Birthday Anime API
# Project Structure
---

This document contains an explanation of the structure of the project, specifying the purpose of each part.

## Document Contents

This document contains:

- **App Structure:** This section explains the overall structure of the application.
- **Test Structure:** This section explains the overall structure of the testing framework.

### App Structure

```
app
  ├── config
  ├── factories
  ├── logs
  ├── middlewares
  ├── models
  │   ├── relationships
  │   └── tables
  ├── repositories
  ├── routers
  │   └── v1
  ├── schemas
  ├── services
  ├── utils
  │   ├── sanatizers
  │   └── validations
  └── validations
```

- **config**: Library configuration, the configuration to connect to the database is currently configured.
- **models**: Contains the entities of the tables and their relationships in the database.
- **utils**: Contains utility functions used throughout the application.
- **schemas**: Contains the structure of the data with which the entities are created, mainly used routes to define the data to be expected and returned
- **repositories**: Contains the functions to interact with the database.
- **factories**: Contains the function to create entity models.
- **validations**: Contains the functions to validate the data before it is processed. It is mainly used in services.
- **services**: Contains the business logic for operations.
- **controllers**: Contains the routes and functions for handling requests and responses.
- **middlewares**: Contains the middleware functions for handling requests and responses.
- **logs**: contains the app.log file with the application logs.

### Test Structure
