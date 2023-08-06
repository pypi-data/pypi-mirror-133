# -*- coding: utf-8 -*-

import inspect
import pkgutil
import os
from pathlib import Path

solvers_path = os.environ.get('OPTILOG_SOLVERS', None)
if solvers_path:
    solvers_path = {Path(s) for s in solvers_path.split(':')}
else:
    solvers_path = set()
solvers_path.add((Path(__file__) / '../solvers').resolve())
solvers_path.add((Path.home() / '.optilog_solvers').resolve())
solvers_path = {str(x.as_posix()) for x in solvers_path}
os.environ['OPTILOG_SOLVERS'] = ':'.join(solvers_path)

# Import pure-python modules/packages
from . import pbencoder
from . import solverbinder

# import classes from extensions submodule
for name, obj in inspect.getmembers(solverbinder):
    if inspect.isclass(obj) and not name.startswith("_"):
        globals()[name] = obj

del inspect
del pkgutil

# from Formulas import CNF, CNFException
# from Formulas import WCNF, WCNFException
# from Formulas import QCNF, QCNFException
# from Formulas import load_from_file
# from Formulas import load_from_stream
# from Formulas import formula_to_1_3_wpm
# from Formulas import generate_3sat_gadget

# from pblib.pb import PB2cnf
# from pbencoder._encoder import Encoder
# from pbencoder.incremental_encoder import IncrementalEncoder


