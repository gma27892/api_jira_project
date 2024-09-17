import json
from jira import JIRA, JIRAError
import pandas as pd
import csv
import re
from datetime import datetime
import random
from faker import Faker

# Reading credentials file JSON
with open('credential_jira.json') as f:
    credentials = json.load(f)

user = credentials['user']
password = credentials['apikey']
link = credentials['link']
project_key = credentials['project_key'] 

# Jira authentication 
jira = JIRA(server=link, basic_auth=(user, password))

# Querying data using JQL language
jql_query = f'project = {project_key} ORDER BY created ASC'

# Pagination of all isseus from Jira project
block_size = 100
block_num = 0

# Opening CSV file for writing all issues in there
print(f"Extracting tickets from {project_key} Jira project...")

with open('jira_issues.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # Writing CSV Column names
    writer.writerow([
        'key', 
        'tool_value',
        'area',
        'sprint',
        'summary', 
        'status', 
        'assignee', 
        'reporter', 
        'created', 
        'updated', 
        #'custom_create_date',
        #'custom_end_date',
        'date_diff_days',
        'priority', 
        'issue_type', 
        #'labels', 
        #'comments', 
    ])

    while True:
        start_idx = block_num * block_size
        try:
            issues = jira.search_issues(jql_query, startAt=start_idx, maxResults=block_size, expand='changelog')
        except JIRAError as e:
            if e.status_code == 404:
                print(f"Ignoring not found tickets {block_num}")
                break  # Quit while if face 404 error
            else:
                raise  # Rerun exception if error was |= from 404 error
        else:
            if not issues:
                break
            for issue in issues:
                # RegExing main custom fileds
                tool_pattern = r"value='(.*?)'"
                tool_match = re.search(tool_pattern, str(issue.fields.customfield_11897)) #Tool
                tool_value = tool_match.group(1) if tool_match else None

                area_pattern = r"value='(.*?)'"
                area_match = re.search(area_pattern, str(issue.fields.customfield_11896)) #Area
                area_value = area_match.group(1) if area_match else None

                sprint_field = issue.fields.customfield_10007
                if isinstance(sprint_field, list):
                    sprint_value = ', '.join([str(sprint) for sprint in sprint_field])
                else:
                    sprint_value = str(sprint_field)

                # Converting dates (Created e Updated) in a date filed
                created_date = datetime.strptime(issue.fields.created, "%Y-%m-%dT%H:%M:%S.%f%z")
                updated_date = datetime.strptime(issue.fields.updated, "%Y-%m-%dT%H:%M:%S.%f%z")
                date_diff_days = (updated_date - created_date).days

                #custom_create_date = datetime.strptime(issue.fields.customfield_11930, "%Y-%m-%dT%H:%M:%S.%f%z")
                #custom_end_date = datetime.strptime(issue.fields.customfield_11931, "%Y-%m-%dT%H:%M:%S.%f%z")

                writer.writerow([
                    issue.key,
                    tool_value,
                    area_value,
                    sprint_value,
                    issue.fields.summary,
                    issue.fields.status.name,
                    issue.fields.assignee.displayName if issue.fields.assignee else 'Unassigned',
                    issue.fields.reporter.displayName,
                    created_date,
                    updated_date,
                    #issue.fields.customfield_11930, #custom_create_date
                    #issue.fields.customfield_11931, #custom_end_date
                    date_diff_days,
                    issue.fields.priority.name if issue.fields.priority else 'None',
                    issue.fields.issuetype.name,
                    #issue.fields.labels if issue.fields.labels else '',
                    #'\n'.join([comment.body for comment in issue.fields.comment.comments]) if issue.fields.comment.comments else '',
                ])
            block_num += 1

df = pd.read_csv('./jira_issues.csv')
no_of_rows = df['key'].count()
print(f"{no_of_rows} tickets were created and written in jira_issues.csv")

interested_columns = ['tool_value', 'area', 'assignee','reporter',]
df = pd.read_csv('./jira_issues.csv',usecols=interested_columns)

distinct_counts = df[interested_columns].nunique()

# Stampare i risultati
print("Count distinct for main columns to anonymizing:")
print(distinct_counts)

# Leggi il file CSV dei problemi Jira
#df = pd.read_csv('./jira_issues.csv')

# Inizializza il generatore di nomi casuali
faker = Faker()

# Dizionario per memorizzare la corrispondenza tra nomi originali e anonimizzati
name_dictionary = {}

# Funzione per anonimizzare un nome
def anonymize_name(name):
    if name not in name_dictionary:
        # Genera un nuovo nome anonimo se non è già stato anonimizzato
        anonymized_name = faker.name()
        name_dictionary[name] = anonymized_name
    return name_dictionary[name]

# Applicare la funzione di anonimizzazione alla colonna 'assignee'
df['anonymized_assignee'] = df['assignee'].apply(anonymize_name)

print(df['anonymized_assignee'])

# Check if the count distinct of the anonymized columsn are the same of original ones

distinct_count_anonymized_assignee = len(set(df['anonymized_assignee']))
print(f"\nUnique values for anonymized_reporter column are: {distinct_count_anonymized_assignee}")

# Esempio di lista di nomi da anonimizzare per i tool
anonymize_tool_list = [
    "Tool A", 
    "Tool B", 
    "Tool C",
    "Tool D", 
    "Tool E", 
    "Tool F",
]

# Dizionario per memorizzare le corrispondenze tra nomi originali e anonimizzati per i tool
tool_dictionary = {}

# Funzione per anonimizzare un tool
def anonymize_tool(tool):
    if tool not in tool_dictionary:
        # Seleziona un nome anonimizzato dalla lista in modo casuale
        anonymized_tool = random.choice(anonymize_tool_list)
        tool_dictionary[tool] = anonymized_tool
    return tool_dictionary[tool]

# Applicare la funzione di anonimizzazione ai tool
df['anonymized_tool'] = df['tool_value'].apply(anonymize_tool)

# Visualizza il DataFrame con le colonne 'assignee_anonymized' e 'anonymized_tool'
print(df['anonymized_tool'])

# Check if the count distinct of the anonymized columsn are the same of original ones

distinct_count_anonymized_tool = len(set(df['anonymized_tool']))
print(f"\nUnique values for anonymized_reporter column are: {distinct_count_anonymized_tool}")

# Esempio di lista di nomi da anonimizzare per i tool
anonymize_area_list = [
    "Marketing",
    "Sales",
    "Finance",
    "Human Resources",
    "Production",
    "Logistics",
    "Research and Development",
    "Customer Service",
    "Project Management",
    "Information Technology (IT)",
    "Quality Assurance",
    "Data Governance",
    "Strategic Planning",
    "Compliance and Regulation",
    "Innovation and Sustainability",
    "Business Intelligence"
]

# Dizionario per memorizzare le corrispondenze tra nomi originali e anonimizzati per i tool
area_dictionary = {}

# Funzione per anonimizzare un tool
def anonymize_area(area):
    if area not in area_dictionary:
        # Seleziona un nome anonimizzato dalla lista in modo casuale
        anonymized_area = random.choice(anonymize_area_list)
        area_dictionary[area] = anonymized_area
    return area_dictionary[area]

# Applicare la funzione di anonimizzazione ai tool
df['anonymized_area'] = df['area'].apply(anonymize_area)

# Visualizza il DataFrame con le colonne 'assignee_anonymized' e 'anonymized_tool'
print(df['anonymized_area'])

# Check if the count distinct of the anonymized columsn are the same of original ones

distinct_count_anonymized_area = len(set(df['anonymized_area']))
print(f"\nUnique values for anonymized_reporter column are: {distinct_count_anonymized_area}")

# Inizializza il generatore di nomi casuali
faker = Faker()

# Dizionario per memorizzare la corrispondenza tra nomi originali e anonimizzati
reporter_dictionary = {}

# Funzione per anonimizzare un nome
def anonymize_reporter(reporter):
    if reporter not in reporter_dictionary:
        # Genera un nuovo nome anonimo se non è già stato anonimizzato
        anonymized_reporter = faker.name()
        reporter_dictionary[reporter] = anonymized_reporter
    return reporter_dictionary[reporter]

# Applicare la funzione di anonimizzazione alla colonna 'assignee'
df['anonymized_reporter'] = df['reporter'].apply(anonymize_reporter)

print(df['anonymized_reporter'])

# Check if the count distinct of the anonymized columsn are the same of original ones

distinct_count_reporter_area = len(set(df['anonymized_reporter']))
print(f"\nUnique values for anonymized_reporter columnare: {distinct_count_reporter_area}")  
