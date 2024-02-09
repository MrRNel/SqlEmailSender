# This file collects all the functions required to construct the reports and centrelize it as a single method
# report_generator.py
from config import excel_file_path, email_recipients,sql_query as sql,business_name  # Import client_names from config.py
from sql_operations import execute_sql_query
from excel_export import export_data_to_excel
from email_sender import send_email
from datetime import datetime

def generate_reports():
    report_paths = []


    # Define the SQL query
    sql_query = sql

    # Execute the SQL query and retrieve data
    df = execute_sql_query(sql_query)

    # Export the data to an Excel file
    excel_file_name = export_data_to_excel(df, excel_file_path)

    report_paths.append(excel_file_name)

    print(f'Data exported to {excel_file_name}')

    # Email details
    email_subject = f'Daily WB Reports For {datetime.now().strftime("%Y-%m-%d_%H:%M")}'
    email_body = f"""
    Hi,

    Please find attached the Weighbridge Report for {datetime.now().strftime("%Y-%m-%d_%H:%M")}.

    Best Regards,
    {business_name} Automation
    """

    # Send a single email with all the attached reports
    if send_email(email_recipients, email_subject, email_body, attachment_file_paths=report_paths, adminEmail=False):
        print(f'Email sent successfully to {", ".join(email_recipients)}')
    else:
        print('Email sending failed.')
