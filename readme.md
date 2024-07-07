# Jira project

<img src="https://upload.wikimedia.org/wikipedia/commons/8/82/Jira_%28Software%29_logo.svg" width="500" />

## Project Description
The Jira Ticket Dashboard is a Python-based project aimed at connecting to the Jira API to download all the tickets from a specified Jira project and display the data in an interactive dashboard. This dashboard will be built using web technologies and can be hosted independently, providing an intuitive interface for users to view and analyze Jira tickets without accessing the Jira site directly.

## Objectives
- **Connect to Jira API**: Authenticate and retrieve data from Jira
- **Data Processing**: Clean and organize the ticket data
- **Dashboard Creation**: Build an interactive dashboard using web frameworks

## Features
- **Authentication**: Securely authenticate to the Jira API
- **Data Retrieval**: Fetch all tickets from a specified Jira project
- **Data Visualization**: Create charts and tables to display ticket statistics
- **Filtering**: Allow users to filter tickets based on various criteria (e.g., status, assignee, date range, etc.)
- **Export Options**: Provide options to export data to CSV or Excel

## Tools and Technologies
- **Programming Language**: Python
- **Libraries**:
  - *Standard Library Modules*:
    - `json`: parses JSON data and converts it to Python dictionaries
    - `csv`: reads/writes from/to CSV files
    - `re`: for regular expression operations
    - `os`: handles operating system functionality like file and directory operations
    - `datetime`: manipulates dates and times
  - *Third-Party Modules*:
    - `pandas`: provides data structures like DataFrames for data manipulation and analysis
    - `sqlalchemy`: facilitates database operations
      - `create_engine`: creates a database connection (imported from `sqlalchemy`)
    - `jira`: : interfaces with the JIRA REST API for issue tracking
      - `JIRAError`: handles errors specific to JIRA interactions (imported from `jira`)


## Output
| | Dashboard | |
|:------:|:------:|:------:|
| [BI Software 1](http://#) | [BI Software 2](http://#) | [BI Software 3](http://#) |
| | | |