import logging 
import requests

logging.basicConfig(level=logging.DEBUG)


def unreleased_workshops():
    """Retorna un listato de los próximos talleres de CódigoFacilito
    
    >>> type(unreleased_workshops()) == type(list())
    True
    """
    response = requests.get('https://codigofacilito.com/api/v2/workshops/unreleased')
    
    try:
        if response.status_code == 200:
            workshops = response.json().get('data')['workshops']
            return workshops

    except Exception as err:
        logging.warning('No fue posible completar la operación.')
        return None