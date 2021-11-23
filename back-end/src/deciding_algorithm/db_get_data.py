import pandas as pd
import random
from faker.providers.person.en import Provider
import numpy as np
import string
import json


def load_json_table(path, as_df=False):
    with open(path) as f:
        d = json.load(f)
    if as_df:
        return pd.DataFrame(d)
    else:
        return d

def update_json_table(path, db):

    if isinstance(db, pd.DataFrame):
        db = db.to_json(orient="records")
        db = json.loads(db)

    with open(path, 'w') as outfile:
        json.dump(db, outfile, indent=4)


def create_absence_request(path):

    employee_id = int(input("Enter your Employee ID: "))
    date_of_absence = str(input("Enter single date for your absence (dd/mm/yyyy): "))

    json_db = load_json_table(path)

    request = {
        "id" : json_db[-1]["id"] + 1,
        "EmployeeID" : employee_id,
        "DateOfAbsence" : date_of_absence,
        "Status" : "Pending"
    }

    json_db.append(request)    
    update_json_table(path,json_db)




def generate_unique_numbers(sample_size, lowest_num = 1,highest_num = 100):
    return random.sample(range(lowest_num, highest_num), sample_size) 


def generate_unique_people_names(sample_size):
    first_names = list(set(Provider.first_names))
    random.seed(4321)
    random.shuffle(first_names)
    return first_names[0:sample_size]


def unique_teams_names(sample_size, team_name_length = 3):
    team_names = []
    for _ in range(sample_size):
        team_names.append(''.join((random.choice(string.ascii_uppercase) for _ in range(team_name_length))))
    return team_names



def create_teams_dict(no_teams):

    teams_ids = generate_unique_numbers(sample_size = no_teams)
    teams_names = unique_teams_names(sample_size = no_teams)
    teams_managers_ids = generate_unique_numbers(sample_size = no_teams, lowest_num = 10000,highest_num = 99999)
    teams_min_capacity = generate_unique_numbers(sample_size = no_teams, lowest_num = 2,highest_num = 5)

    teams = []
    for team_id, team_name, team_manager_id, team_min_capacity in zip(teams_ids, teams_names, teams_managers_ids, teams_min_capacity):
        team = dict()
        team["OUID"] = team_id
        team["ManagerID"] = team_manager_id
        team["MinimalCapacity"] = team_min_capacity
        team["TeamName"] = team_name
        teams.append(team)

    return teams

def create_employees_dict(no_people, teams_dict):


    employees_ids = generate_unique_numbers(sample_size = no_people)
    employees_names = unique_teams_names(sample_size = no_people)
    employees_employment_no = [random.randint(1,3) for _ in range(no_people)]
    employees_ouids = generate_unique_numbers(sample_size = no_people, lowest_num = 10000,highest_num = 99999)

    employees = []

    for employee_id, employee_name, employee_employment_no, employee_ouid in zip(employees_ids, employees_names, employees_employment_no, employees_ouids):
        employee = dict()
        employee["EmployeeID"] = employee_id
        employee["EmployeeName"] = employee_name
        employee["EmploymentNumber"] = employee_employment_no
        employee["OUID"] = employee_ouid
        employees.append(employee)

    return employees



def main():

    teams = create_teams_dict(2)
    employees = create_employees_dict(20, teams)


if __name__ == "__main__":
    main()




