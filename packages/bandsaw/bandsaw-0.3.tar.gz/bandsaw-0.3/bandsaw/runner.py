"""Contains main() function to continue sessions from files"""
import argparse
import io
import logging
import os

from .run import set_run_id
from .session import Session


logger = logging.getLogger(__name__)


def main(args):
    """
    Main function that can be used for proceeding a session.

    This function allows to read a session from a file, proceed it until it returns
    and then save the state of the session to a new file. It is used for running
    tasks in a separate process or on different machines.

    Args:
        args (tuple[str]): The arguments taken from the command line.
    """
    hostname = os.uname()[1]
    log_format = (
        f"{{asctime}} {hostname} {{process: >5d}} {{thread: >5d}} "
        f"{{name}} {{levelname}}: {{message}}"
    )
    logging.basicConfig(level=logging.INFO, format=log_format, style='{')

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input',
        dest='input_session',
        help="The session which should be continued",
        required=True,
    )
    parser.add_argument(
        '--output',
        dest='output_session',
        help="The session after continuation ended",
        required=True,
    )
    parser.add_argument(
        '--run-id',
        dest='run_id',
        help="The run id of the workflow",
        required=True,
    )
    args = parser.parse_args(args=args)

    set_run_id(args.run_id)

    logger.info("Creating new session")
    session = Session()

    logger.info("Reading session from %s", args.output_session)
    with io.FileIO(args.input_session, mode='r') as stream:
        session.restore(stream)

    logger.info("Proceeding session")
    session.proceed()

    logger.info("Writing session with result to %s", args.output_session)
    with io.FileIO(args.output_session, mode='w') as stream:
        session.save(stream)
