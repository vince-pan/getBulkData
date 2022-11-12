# coding: utf-8
"""
Main Bulk class.  Defines:
  - Bulk
  - Part2D
  - Fastener
  - Junction
"""

import os
from pyNastran.bdf.bdf import BDF


class Bulk(BDF):
    """

    """
    pass


if __name__ == '__main__':
    test_path = os.path.join('..', 'models')
    bdf_filename = os.path.join(test_path, 'FEM-001.bdf')
    model = BDF()
    model.read_bdf(bdf_filename)