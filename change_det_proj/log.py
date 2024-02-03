import logging
import os

def log_to_file(message):
    log_file_path = os.path.join(os.getcwd(), 'logfile.txt')
    logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    # Log the message
    logging.info(message)