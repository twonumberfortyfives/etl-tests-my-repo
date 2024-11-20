# Preliminary Task: Junior Test Engineer

Welcome to the preliminary task for the Junior Test Engineer at Reagle! This task is desined to check what approaches the potential applicant is to take when testing a simple Extract-Transform-Load datapipeline.

## Task Overview

In this task, you're job is to go trough a data pipeline that a lazy dataengineer wrote in a hurry and check that everythin is working. Write the most relevant test cases for this particular example. The test can be unittests, end-to-end tests or data validations. You do not need to implement everything. Just show us some approach and please do not spend too much time on this, we sure did not spend too much time writing this either.

### Requirements

- sqlite3
- python3.10 or later

## How to Get Started

### 1. Clone the Repository

First, clone this repository to your local machine:

```bash
git clone git@github.com:reaglecode/test-case-preliminary-task.git
cd test-case-preliminary-task
```

### 2. Install Requirements

Next install requirements. It is recommended to create a virtual enviroment first. Remember to install also your preferred testing library/libraries.

```bash
pip install -r requirements.txt
```

### 3. Initialise the database and run the ETL

```bash
python main --method init
python main
```














