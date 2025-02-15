#### Birthday Anime API
# SonarQube
---

This document contains information about the SonarQube application and how to use it for the project.

## Document Content

This document includes:

- **About SonarQube**: What is SonarQube and what is its function?
- **How to install SonarQube**: SonarQube installation
- **SonarScanner**: What it is and how to use it
- **Scan configuration**: Configuration of the `sonar-project.properties` file for project scanning
- **Commands**: How to scan the project

### About SonarQube

SonarQube is an open-source platform developed by SonarSource that continuously inspects code quality.
It performs static code analysis to detect bugs, vulnerabilities, and code smells in your source code,
while also measuring metrics like duplications, complexity, and test coverage. This helps teams maintain
high-quality, secure, and maintainable code over time.

### How to install SonarQube

During the development of the project I used SonarQube using docker which I recommend for a quick and
trouble-free installation. [SonarQube Documentation](https://docs.sonarsource.com/sonarqube-community-build/)

### SonarScanner

SonarScanner is a command-line tool that runs a static analysis on your source code and then sends the analysis
results—such as bugs, vulnerabilities, code smells, and other quality metrics—to a SonarQube or SonarCloud server
for further processing and visualization.

The installation of this tool is important, so I attach the following
[link](https://docs.sonarsource.com/sonarqube-server/latest/analyzing-source-code/analysis-parameters/)
for its installation

### Scan configuration

The `sonar-project.properties` file allows you to define parameters for scanning such as connection to the
sonarqube application, project identification tags, path definition, exclusion of files that should not be
scanned, etc.

If you wish to learn more, I invite you to access the documentation
[Link](https://docs.sonarsource.com/sonarqube-server/latest/analyzing-source-code/analysis-parameters/)

### Commands

To scan the project, the following command must be executed:

```bash
sonar-scanner -Dsonar.login=TOKEN
```

To obtain the `TOKEN` you must login to SonarQube go to My Account>Security and create a global analysis token
to enable SonarScanner to authenticate to SonarQube.

The results of the analysis can be viewed in the project dashboard by selecting the name of the project.
