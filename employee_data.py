# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "faker",
# ]
# ///
import csv
from faker import Faker

# Set a random seed for reproducibility
faker = Faker()
faker.seed_instance(42)


# Define function to generate employee data
def generate_employee_data():
    employee_id = faker.random_number(digits=6)
    first_name = faker.first_name()
    last_name = faker.last_name()
    gender = faker.random_element(['Male', 'Female'])
    dob = faker.date_of_birth(minimum_age=18, maximum_age=65)
    job_title = faker.job()
    department = faker.random_element(['Engineering', 'HR', 'Finance', 'Marketing', 'Sales', 'Operations'])
    manager_name = f"{faker.first_name()} {faker.last_name()}"
    hire_date = faker.date_between(start_date='-10y', end_date='today')
    email = faker.email()
    phone_number = faker.phone_number()
    address = faker.street_address()
    city = faker.city()
    state = faker.state()
    country = faker.country()
    postal_code = faker.postcode()
    salary = faker.random_int(min=40000, max=150000)
    employee_status = faker.random_element(['Active', 'Inactive'])
    performance_rating = faker.random_int(min=1, max=5)

    # Termination date only if employee is inactive
    if employee_status == 'Inactive':
        termination_date = faker.date_between(start_date=hire_date, end_date='today')
    else:
        termination_date = None

    return [
        employee_id, first_name, last_name, gender, dob, job_title, department, manager_name,
        hire_date, email, phone_number, address, city, state, country, postal_code, salary,
        employee_status, termination_date, performance_rating
    ]

# Define function to write employee data to CSV
def write_to_csv(filename, num_records):
    fields = [
        'Employee ID', 'First Name', 'Last Name', 'Gender', 'Date of Birth', 'Job Title', 'Department',
        'Manager Name', 'Hire Date', 'Email', 'Phone Number', 'Address', 'City', 'State', 'Country',
        'Postal Code', 'Salary', 'Employee Status', 'Date of Termination', 'Performance Rating'
    ]

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(fields)

        for _ in range(num_records):
            writer.writerow(generate_employee_data())

    print(f"Generated {num_records} employee records in '{filename}'.")

# Generate 2,000 employees and write to CSV
write_to_csv('employee_data.csv', 2000)
