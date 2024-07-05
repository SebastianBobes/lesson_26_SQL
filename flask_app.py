from flask import Flask, request

import company_func

app = Flask(__name__)
config = company_func.initialise_config()

@app.route("/", methods=['GET'])
def first_function():
    return {"message": "Hello Word!"}

@app.route(rule = "/home", methods=['PUT', 'POST'])
def second_function():
    print(request.method)
    data=request.json
    print(data['name'])
    return {"message": "Post or put request"}

@app.route("/emps/<emp_id>")
def get_employees(emp_id):
    if emp_id:
        sql_query = f"SELECT * from company.employees where emp_id ={emp_id}"
        return company_func.read_from_database(sql_query, config)


if __name__ == '__main__':
    app.run()
