"""
Python kit information provider for Microchip development kits
"""
# Python 3 compatibility for Python 2
from __future__ import print_function

# args, logging
import sys
import argparse
import os
import logging
from logging.config import dictConfig
from pathlib import Path
import textwrap
import yaml


from appdirs import user_log_dir
from yaml.scanner import ScannerError

# pykitinfo main function
from . import pykitinfo

def setup_logging(user_requested_level=logging.ERROR, default_path='logging.yaml',
                  env_key='MICROCHIP_PYTHONTOOLS_CONFIG'):
    """
    Setup logging configuration for pykitinfo CLI
    """
    # Logging config YAML file can be specified via environment variable
    value = os.getenv(env_key, None)
    if value:
        path = value
    else:
        # Otherwise use the one shipped with this application
        path = os.path.join(os.path.dirname(__file__), default_path)
    # Load the YAML if possible
    if os.path.exists(path):
        try:
            with open(path, 'rt') as file:
                # Load logging configfile from yaml
                configfile = yaml.safe_load(file)
                # File logging goes to user log directory under Microchip/modulename
                logdir = user_log_dir(__name__, "Microchip")
                # Look through all handlers, and prepend log directory to redirect all file loggers
                num_file_handlers = 0
                for handler in configfile['handlers'].keys():
                    # A filename key
                    if 'filename' in configfile['handlers'][handler].keys():
                        configfile['handlers'][handler]['filename'] = os.path.join(
                            logdir, configfile['handlers'][handler]['filename'])
                        num_file_handlers += 1
                # If file logging is enabled, it needs a folder
                if num_file_handlers > 0:
                    # Create it if it does not exist
                    Path(logdir).mkdir(exist_ok=True, parents=True)
                # Console logging takes granularity argument from CLI user
                configfile['handlers']['console']['level'] = user_requested_level
                # Root logger must be the most verbose of the ALL YAML configurations and the CLI user argument
                most_verbose_logging = min(user_requested_level, getattr(logging, configfile['root']['level']))
                for handler in configfile['handlers'].keys():
                    # A filename key
                    if 'filename' in configfile['handlers'][handler].keys():
                        level = getattr(logging, configfile['handlers'][handler]['level'])
                        most_verbose_logging = min(most_verbose_logging, level)
                configfile['root']['level'] = most_verbose_logging
            dictConfig(configfile)
            return
        except ScannerError:
            # Error while parsing YAML
            print("Error parsing logging config file '{}'".format(path))
        except KeyError as keyerror:
            # Error looking for custom fields in YAML
            print("Key {} not found in logging config file".format(keyerror))
    else:
        # Config specified by environment variable not found
        print("Unable to open logging config file '{}'".format(path))

    # If all else fails, revert to basic logging at specified level for this application
    print("Reverting to basic logging.")
    logging.basicConfig(level=user_requested_level)

# Helper functions
def _parse_literal(literal):
    """
    Literals can either be integers or float values.  Default is Integer
    """
    try:
        return int(literal, 0)
    except ValueError:
        return float(literal)

def main():
    """
    Entrypoint for installable CLI

    Configures the CLI and parses the arguments
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\

    Basic actions:
            '''),
        epilog=textwrap.dedent('''\
    Usage examples:
        
            '''))

    parser.add_argument("-l", "--long", action="store_true",
                        help="Show long list")

    parser.add_argument("-b", "--brief", action="store_true",
                        help="Show only serial port mapping for detected matching units")

    parser.add_argument("-v", "--verbose",
                        default="warning", choices=['debug', 'info', 'warning', 'error', 'critical'],
                        help="Logging verbosity level")

    parser.add_argument("-V", "--version",
                        help="Print pykitinfo version number and exit",
                        action="store_true")

    parser.add_argument("-R", "--release-info", action="store_true",
                        help="Print pykitinfo release details and exit")

    parser.add_argument("-s", "--serialnumber",
                        type=str,
                        help="USB serial number of the unit to use")

    # Parse args
    arguments = parser.parse_args()

    # Setup logging
    setup_logging(user_requested_level=getattr(logging, arguments.verbose.upper()))
    logger = logging.getLogger(__name__)
    try:
        # Call main with args
        return pykitinfo.pykitinfo(arguments)
    except Exception as exc:
        logger.error("Operation failed with %s: %s", type(exc).__name__, exc)
        logger.debug(exc, exc_info=True)    # get traceback if debug loglevel
    return pykitinfo.STATUS_FAILURE

if __name__ == "__main__":
    sys.exit(main())
