#### Birthday Anime API
# Initialize Project
---

Welcome to the repository initialization documentation. This document describes the process for starting the
project locally, detailing the necessary steps and providing relevant information about the content of this file.

## Document Contents

This document includes:

- **Prerequisites:** List of tools, versions and dependencies needed.
- **Installation and Configuration:** Step-by-step guide to clone, install dependencies, configure environment
variables and run the project.
- **Additional Notes:** Tips, solutions to common problems and links to external documentation.

## Prerequisites:
- Python 3.12
- pip 3.12

## Installation and Configuration
- Clone the repository:
  ```bash
  git clone https://github.com/BOTHIKIGAI/BACK-API-BIRTDAY-ANIME
  cd BACK-API-BIRTDAY-ANIME
  ```
- Create a virtual environment:
  ```bash
  python -m venv venv
  source venv/bin/activate
  ```
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```
- Configure environment variables:
  ```bash
  cp .env.example .env
  ```
- Run the project:
  ```bash
  uvicorn main:app --reload
  ```

## Additional Notes
The configuration of the environment variables inside the `.env` file is important to start the project. In case you don't have them you can add any value in order not to handle null data.
