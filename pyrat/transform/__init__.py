# Transform __init__
import logging
from .Flip import *
from .Crop import *


def info():
    import sys
    from inspect import getmembers, isclass
    current_module = sys.modules[__name__]
    modules = getmembers(current_module, isclass)
    logging.info('')
    logging.info("Content of module "+__name__+":")
    logging.info('')
    for mod in modules:
        if 'PyRat' in mod[1].__module__:
            doc = str(mod[1].__doc__)
            if doc != 'None':
                doc = doc.split('\n')[1]
            logging.info(mod[0].ljust(20)+doc)
