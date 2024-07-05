import json
import psycopg2 as ps
import base64 as b64



def initialise_config():
    with open("config.json", "r") as f:
        config = json.loads(f.read())
        config['password'] = b64.b64decode(config['password']).decode()
    return config


def read_from_database(sql_query: str,config: dict):
    try:
        with ps.connect(**config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_query)
                response = cursor.fetchall()
                columns = [item.name for item in cursor.description]
                new_data = []
                for employee in response:
                    new_data.append(dict(zip(columns, employee)))
                return new_data
    except Exception as e:
        print(f"Failure on reading from database. Error: {e}")

def execute_query(sql_query: str, config: dict):
    try:
        with ps.connect(**config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_query)
                return True
    except Exception as e:
        print(f"Failure on reading from database. Error: {e}")
        return False


if __name__ == '__main__':
    budget_cap = 0.8
    MENU = """
    1.SHOW ALL EMPLOYEES.
    2.SHOW ALL EMPLOYEES BY DEPARTMENT.
    3.SHOW ALL PROJECTS OF A CERTAIN EMPLOYEE.
    4.CHANGE SALARY TO EMPLOYEE.
    5.HIRE NEW EMPLOYEE.
    6.FIRE NEW EMPLOYEE.
    7.EXIT 
    """
    config = initialise_config()
    while True:
        user_pick = int(input(MENU))
        match user_pick:
            case 1:
                emps = read_from_database(sql_query="select * from company.employees", config=config)
                print(json.dumps(emps, indent=4))
            case 2:
                departments = read_from_database(sql_query="select * from company.departments", config=config)
                for department in departments:
                    print(f"{department['department_id']}.{department['name']}")
                department_pick = input("Choose a department: ")
                emps = read_from_database(f"select * from company.employees where department_id = {department_pick}", config)
                print(json.dumps(emps, indent=4))
            case 3:
                pass
            case 4:
                emp = {}
                emps = read_from_database(sql_query="select * from company.employees", config=config)
                for emp in emps:
                    print(f"{emp['emp_id']}.{emp['name']}")
                emp_pick = input()
                for emp in emps:
                    if emp_pick == emp['emp_id']:
                        break
                available_budget_quey =f"""
                                            select sum(p.budget) from company.projects p
                                            join company.contracts c on c.project_id =p.project_id
                                            join company.employees e on e.emp_id =c.emp_id
                                            where e.emp_id ={emp_pick};"""
                budget = read_from_database(available_budget_quey, config)
                percentage = input("What is the raise in percentage?")
                new_salary = emp['salary'] + emp['salary']*(float(percentage)/100)
                if new_salary < budget[0]['sum']* budget_cap:
                    execute_query(f"UPDATE company.employees set salary = {new_salary} where emp_id = {emp_pick}", config)
                else:
                    print("Not enough money for the raise!")

            case 5:
                emps = read_from_database(sql_query="select emp_id,name from company.employees", config=config)
                departments= read_from_database(sql_query="select department_id, name from company.departments", config=config)
                for department in departments:
                    print(f"{department['department_id']}. {department['name']}")
                department_choice = input()
                new_emp_data = input("Enter all data about employee: name/date of birth/salary/starting date")
                new_emp_data=new_emp_data.split("/")
                if new_emp_data[0] not in str(emps):
                    query = (f"INSERT into company.employees(name, date_of_birth, salary, starting_date, department_id)"
                             f"values ('{new_emp_data[0]}', '{new_emp_data[1]}', {new_emp_data[2]}, '{new_emp_data[3]}', {department_choice})")
                    execute_query(query, config)


            case 6:
                emps = read_from_database(sql_query="select emp_id,name from company.employees", config=config)
                for emp in emps:
                    print(f"{emp['emp_id']}.{emp['name']}")
                emp_pick = input()
                consent = input("Are you sure you want to fire this employee? Y/N ")
                if consent.lower() == "y":
                    execute_query(f"DELETE from company.employees where emp_id = {emp_pick}", config)
            case 7:
                exit()
            case _:
                exit()
#2:08:04

