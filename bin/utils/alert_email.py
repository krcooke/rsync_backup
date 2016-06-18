#!/usr/bin/python

# To do
# Collect all of the messages together
# Grab teh configs from the config file

import email
import smtplib
from time import gmtime, strftime
from utils.config import get_email_smtp, get_email_smtp_port, get_email_username, get_email_password, get_email_target, get_delete_limit
import logging

logger = logging.getLogger('rsync_backup')

message = None

def send_email():
    global message

    if message == None:
        return
    logger.debug(message)

    msg = email.message_from_string(message)
    msg['From'] = get_email_username()
    msg['To'] = get_email_target()
    msg['Subject'] = "Backup Alert "+strftime("%Y-%m-%d", gmtime())

    s = smtplib.SMTP(get_email_smtp(),get_email_smtp_port())
    s.ehlo() # Hostname to send for this command defaults to the fully qualified domain name of the local host.
    s.starttls() #Puts connection to SMTP server in TLS mode
    s.ehlo()
    s.login(get_email_username(), get_email_password())

    s.sendmail(get_email_username(), get_email_target(), msg.as_string())
    s.quit()

def add_message(command_pair, count_of_files_to_delete):
    global message

    if message == None:
        limit = get_delete_limit()
        message = "More than {limit} files have been marked for deletion, manual backup required\n".format(limit=str(limit))

    message += """
        Number of files marked for deletion: {count}
        Manual noexec command:
            {noexec}

        Manual exec command:
            {exec}\n""".format(count=str(count_of_files_to_delete), noexec=command_pair[0], exec=command_pair[1])
