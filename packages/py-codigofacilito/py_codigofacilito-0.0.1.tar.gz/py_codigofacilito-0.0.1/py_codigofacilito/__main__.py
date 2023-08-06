import logging
from py_codigofacilito import unreleased_workshops

def workshops():
    for workshop in unreleased_workshops():
        logging.debug(workshop['workshop']['title'])


if __name__ == '__main__':
    workshops()
    