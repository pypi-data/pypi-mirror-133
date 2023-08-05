# pyxtend

Some functions to make Python more productive.

## TODO
* Add numpy to requirements
* Add rest of functions
* Update the __init__ or __all__ file so it can be imported with from pyxtend import struct
* Needs better performance on cases like np.zeros((10000, 2, 256, 256, 3))
** Should it only do the extra thing for sets?

## Adding New Package to PyPI

* Update version in setup.cfg
* Upgrade build
 * (Windows): `py -m pip install --upgrade build`
 * (Mac/Linux): `python3 -m pip install --upgrade build`
* Build
 * (Windows): `py -m build`
