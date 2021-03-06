#!/usr/bin/python3.5

import yaml
import os.path
import logging

logger = logging.getLogger('rsync_backup')

config = None
cmd = '/usr/bin/rsync'


# load the configuration file in
def load_config(filepath):
    global config
    with open(filepath, "r") as file_descriptor:
        config = yaml.load(file_descriptor)
    logger.debug("Config: ", config)

# Returns a list of tuplets (of commands src and destination)
def get_commands():
    logger.debug("Config: ", config)
    locations = config['backup']['locations']
    commands = []

    # Test to see if the source and destination locations exist/are accessible
    _test_locations()

    # Compile the commands
    commands = [(_get_cmd(location['src'],location['dest'], 'noexec'),_get_cmd(location['src'],location['dest'],'exec')) for location in locations]
    _print_commands(commands)
    return commands

def _get_cmd (source, destination, mode='noexec'):
    params = config['backup']['commands'][mode]
    noexec_cmd = [cmd]
    noexec_cmd += params
    noexec_cmd += (source, destination)
    #noexec_cmd_str = " ".join(noexec_cmd)
    return noexec_cmd

def _test_locations():
    locations = config['backup']['locations']
    # Test to see if the source and destination locations exist/are accessible
    bad_locations = [(os.path.exists(location['src']), location['src']) for location in locations]
    bad_locations += ([(os.path.exists(location['dest']), location['dest']) for location in locations])
    logger.debug(bad_locations)

    for location in bad_locations:
        if not location[0]:
            logger.debug('Error location ' + location[1] + " does not exist")
    if len([location for location in bad_locations if not location[0]]) > 0:
        logger.debug("One or more locations are not accessible, existing")
        #exit()

def _print_commands(commands):
    logger.debug("Commands:")
    for command_pair in commands:
        logger.debug("Noexec: %s", command_pair[0])
        logger.debug("Exec: %s", command_pair[1])


def get_log_path():
    if config == None: exit("You must load the config first")
    return config['backup']['log']

def get_delete_limit():
    if config == None: exit("You must load the config first")
    return config['backup']['delete_limit']

def get_email_smtp():
    if config == None: exit("You must load the config first")
    return config['backup']['email']['smtp']

def get_email_smtp_port():
    if config == None: exit("You must load the config first")
    return config['backup']['email']['smtp_port']

def get_email_username():
    if config == None: exit("You must load the config first")
    return config['backup']['email']['username']

def get_email_password():
    if config == None: exit("You must load the config first")
    return config['backup']['email']['password']

def get_email_target():
    if config == None: exit("You must load the config first")
    return config['backup']['email']['target']

