# coding: utf-8
"""the interface for bulk_test"""

import os
from bulk.bulk import Bulk


def test_read_bulk(model_filename):
    """read_bulk test """
    # create instance of class Bulk
    bulk = Bulk()
    # read testing model
    bulk.read_bulk(model_filename)
    # print model stat
    # print(bulk.get_bdf_stats())
    # print test
    print(bulk.part_2d[16].elements)


def main():
    """the interface for bulk_test"""
    # set file name of testing model
    test_path = os.path.join('..', '..', 'models')
    bdf_filename = os.path.join(test_path, 'FEM-001.bdf')

    # read testing model
    test_read_bulk(bdf_filename)


if __name__ == '__main__':
    main()
