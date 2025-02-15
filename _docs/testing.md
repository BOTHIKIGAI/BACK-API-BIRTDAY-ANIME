#### Birthday Anime API
# Testing
---

This document describes the tools, commands and configurations performed for the execution of the tests.

## Document Content

This document includes:

- **Libraries**: Libraries used in the project.
- **Configurations**: Configurations used in the project.
- **Commands**: Tools and commands used in the project.

### Libraries

- Pytest 8.3.4
- Pytest-cov 4.0.0

### Configurations

- **Pytest**: The pytest.ini file contains the settings for the execution of the tests, defining file paths, test naming convention and the project directory path.
- **Pytest-cov**: The .coveragerc file contains the configuration for the creation of the unit test report which is mainly used to be processed by SonarQube (software quality analysis tool).

### Commands

- To run the tests (Must be performed in the root of the project)

```shell
pytest
```

- To obtain test coverage (Must be performed in the root of the project)

```shell
pytest --cov-report=xml
```
