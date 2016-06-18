#!/usr/bin/python

from subprocess import run, CalledProcessError, PIPE
from re import match
import sys
import argparse
import logging
from utils.config import load_config, get_commands, get_log_path, get_delete_limit
from utils.alert_email import send_email, add_message
from utils.logger import setupLogger

# Parse the input params
parser = argparse.ArgumentParser()
parser.add_argument("--verbose", help="Run in debug mode", action="store_true")
parser.add_argument("--config-file", help="Config file", type=str, default="../etc/config.yml")
args = parser.parse_args()

# Logging
config_file = args.config_file
load_config(config_file)
log_path = get_log_path()
setupLogger(log_path, args.verbose)
logger = logging.getLogger('rsync_backup')

# Generate the commands
commands = get_commands()

for command_pair in commands:
    logger.debug("Noexec: %s", command_pair[0])
    logger.debug("Exec: %s", command_pair[1])

    # Work out how many files there are to delete
    try:
        status = run(command_pair[0], stdout=PIPE, universal_newlines=True )
    except CalledProcessError as e:
        logger.error ("STDout: %s", CalledProcessError.output)
    output = status.stdout
    logger.debug(output)

    files_to_delete = [line.rstrip() for line in output.split("\n") if match( r'^\*deleting', line)]
    logger.debug(files_to_delete)

    count_of_files_to_delete = len(files_to_delete)
    logger.debug("Files to delete: %s", count_of_files_to_delete)

    delete_limit = get_delete_limit()
    if count_of_files_to_delete > 50:
        add_message(command_pair, count_of_files_to_delete)
    else:
        try:
            status = run(command_pair[1])
        except CalledProcessError as e:
            logger.error ("STDout: %s", CalledProcessError.output)

send_email()