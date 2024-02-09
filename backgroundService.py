import time
import servicemanager
import socket
import sys
import os
import win32serviceutil
import win32service
from report_generator import generate_reports # Import your function here
from email_sender import send_email
from config import admin_email_recipients, SCHEDULED_TIMES ,business_name
from datetime import datetime

class MyDaemonService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'BoulderEmailService'
    _svc_display_name_ = 'BoulderEmailService'

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.is_alive = True

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.is_alive = False

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def main(self):
        while self.is_alive:
            current_time = time.localtime()
            current_hour_minute = (current_time.tm_hour, current_time.tm_min)

            if current_hour_minute in SCHEDULED_TIMES:
                self.my_function()

            time.sleep(60)

    def my_function(self):
        # Call your function to generate reports
        generate_reports()
          # Email details
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
        email_subject = f'{business_name} Report'
        email_body = f"""
        Hi,

        Reports sent: {current_date}

        Best Regards
        {business_name} Automation
        """

        # Send a single email with all the attached reports
        if send_email(admin_email_recipients, email_subject, email_body, adminEmail=True):
            print(f'Email sent successfully to {", ".join(admin_email_recipients)}')        


if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(emonService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(MyDaemonService)
