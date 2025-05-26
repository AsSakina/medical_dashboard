import json
import os
import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Generate random date within range
def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)

# Format date to YYYY-MM-DD
def format_date(date):
    return date.strftime('%Y-%m-%d')

# Generate patient data
def generate_patient_data(days=90):
    patients = []
    now = datetime.now()
    departments = ['Cardiology', 'Neurology', 'Oncology', 'Pediatrics', 'Emergency', 'Surgery']
    treatments = ['Medication', 'Surgery', 'Therapy', 'Observation', 'Intensive Care']
    outcomes = ['Recovered', 'Improved', 'Stable', 'Deteriorated', 'Deceased']
    outcome_weights = [0.6, 0.2, 0.1, 0.07, 0.03]  # Probability weights

    for i in range(1000):
        admission_date = random_date(now - timedelta(days=days), now)
        stay_duration = random.randint(1, 30)
        discharge_date = admission_date + timedelta(days=stay_duration)
        
        # Determine if patient is still admitted
        is_admitted = discharge_date > now
        
        department = random.choice(departments)
        treatment = random.choice(treatments)
        
        # Weighted random outcome selection
        if is_admitted:
            outcome = 'In Treatment'
        else:
            outcome = random.choices(outcomes, weights=outcome_weights)[0]
        
        # Generate costs based on department and treatment
        base_cost = {
            'Cardiology': 1500,
            'Neurology': 1800,
            'Oncology': 2200,
            'Pediatrics': 1000,
            'Emergency': 2000,
            'Surgery': 3000
        }.get(department, 1200)
        
        if treatment == 'Surgery':
            base_cost += 5000
        if treatment == 'Intensive Care':
            base_cost += 3000
        
        treatment_cost = base_cost * (0.8 + random.random() * 0.4) * stay_duration
        
        patients.append({
            'patientId': f'P{1000 + i}',
            'age': random.randint(1, 95),
            'gender': random.choice(['Male', 'Female']),
            'department': department,
            'admissionDate': format_date(admission_date),
            'dischargeDate': None if is_admitted else format_date(discharge_date),
            'stayDuration': (now - admission_date).days if is_admitted else stay_duration,
            'treatment': treatment,
            'outcome': outcome,
            'treatmentCost': round(treatment_cost),
            'insuranceCovered': round(treatment_cost * (0.7 + random.random() * 0.25)),
            'isAdmitted': is_admitted
        })
    
    return patients

# Generate staff data
def generate_staff_data():
    departments = ['Cardiology', 'Neurology', 'Oncology', 'Pediatrics', 'Emergency', 'Surgery', 'Administration']
    roles = ['Doctor', 'Nurse', 'Technician', 'Administrative', 'Support']
    staff = []
    
    for i in range(200):
        department = random.choice(departments)
        role = random.choice(roles)
        
        # Base salary by role
        base_salary = {
            'Doctor': 120000,
            'Nurse': 70000,
            'Technician': 60000,
            'Administrative': 50000,
            'Support': 40000
        }.get(role, 45000)
        
        # Adjust by department
        if department in ['Surgery', 'Cardiology']:
            base_salary *= 1.2
        
        years_of_service = random.randint(0, 30)
        # Salary increases with years of service
        salary = round(base_salary * (1 + years_of_service * 0.02))
        
        staff.append({
            'staffId': f'S{1000 + i}',
            'department': department,
            'role': role,
            'yearsOfService': years_of_service,
            'salary': salary,
            'patientsHandled': random.randint(10, 100) if role in ['Doctor', 'Nurse'] else 0,
            'performanceScore': round(random.uniform(70, 100) / 100, 2)
        })
    
    return staff

# Generate department performance data
def generate_department_data(patient_data, staff_data):
    departments = ['Cardiology', 'Neurology', 'Oncology', 'Pediatrics', 'Emergency', 'Surgery']
    department_data = []
    
    for dept in departments:
        dept_patients = [p for p in patient_data if p['department'] == dept]
        dept_staff = [s for s in staff_data if s['department'] == dept]
        
        total_patients = len(dept_patients)
        if total_patients > 0:
            avg_stay_duration = sum(p['stayDuration'] for p in dept_patients) / total_patients
        else:
            avg_stay_duration = 0
            
        total_revenue = sum(p['treatmentCost'] for p in dept_patients)
        total_salaries = sum(s['salary'] for s in dept_staff)
        
        # Calculate recovery rate
        non_admitted = [p for p in dept_patients if not p['isAdmitted']]
        recovered_patients = len([p for p in non_admitted if p['outcome'] in ['Recovered', 'Improved']])
        recovery_rate = recovered_patients / len(non_admitted) if len(non_admitted) > 0 else 0
        
        # Calculate bed utilization
        beds_available = {
            'Cardiology': 50,
            'Neurology': 40,
            'Oncology': 60,
            'Pediatrics': 45,
            'Emergency': 30,
            'Surgery': 35
        }[dept]
        
        currently_admitted = len([p for p in dept_patients if p['isAdmitted']])
        bed_utilization = currently_admitted / beds_available
        
        department_data.append({
            'department': dept,
            'totalPatients': total_patients,
            'avgStayDuration': round(avg_stay_duration, 2),
            'totalRevenue': total_revenue,
            'totalSalaries': total_salaries,
            'operatingCost': total_salaries + random.randint(50000, 200000),  # Add other costs
            'recoveryRate': round(recovery_rate, 2),
            'bedsAvailable': beds_available,
            'currentlyAdmitted': currently_admitted,
            'bedUtilization': round(bed_utilization, 2),
            'staffCount': len(dept_staff),
            'doctorCount': len([s for s in dept_staff if s['role'] == 'Doctor']),
            'nurseCount': len([s for s in dept_staff if s['role'] == 'Nurse'])
        })
    
    return department_data

# Generate daily metrics for time series
def generate_daily_metrics(days=90):
    daily_metrics = []
    now = datetime.now()
    
    for i in range(days):
        date = now - timedelta(days=days-i)
        
        daily_metrics.append({
            'date': format_date(date),
            'newAdmissions': random.randint(5, 25),
            'discharges': random.randint(5, 20),
            'emergencyVisits': random.randint(20, 60),
            'surgeries': random.randint(3, 15),
            'revenue': random.randint(50000, 150000),
            'expenses': random.randint(40000, 120000)
        })
    
    return daily_metrics

# Generate all data and save to JSON files
def generate_all_data():
    patient_data = generate_patient_data()
    staff_data = generate_staff_data()
    department_data = generate_department_data(patient_data, staff_data)
    daily_metrics = generate_daily_metrics()
    
    # Create data directory if it doesn't exist
    if not os.path.exists('./data'):
        os.makedirs('./data')
    
    with open('./data/patients.json', 'w') as f:
        json.dump(patient_data, f, indent=2)
    
    with open('./data/staff.json', 'w') as f:
        json.dump(staff_data, f, indent=2)
    
    with open('./data/departments.json', 'w') as f:
        json.dump(department_data, f, indent=2)
    
    with open('./data/daily_metrics.json', 'w') as f:
        json.dump(daily_metrics, f, indent=2)
    
    print('Generated fictive health structure data:')
    print(f'- {len(patient_data)} patient records')
    print(f'- {len(staff_data)} staff records')
    print(f'- {len(department_data)} department performance records')
    print(f'- {len(daily_metrics)} days of daily metrics')
    print('Data saved to ./data/ directory')

if __name__ == "__main__":
    generate_all_data()