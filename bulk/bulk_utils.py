# coding: utf-8

import os
from bulk.bulk import Bulk


def extend_elements_from_nids(bulk, nids):
    """

    :param bulk: instance of class Bulk
    :param nids: list of node ids
    :return:
    """
    return {}


def main():
    """the interface for bulk_test"""
    # set file name of testing model
    test_path = os.path.join('..', '..', 'models')
    bdf_filename = os.path.join(test_path, 'FEM-001.bdf')

    # create instance of class Bulk
    bulk = Bulk()
    # read testing model
    bulk.read_bulk(bdf_filename)
    #
    part = extend_elements_from_nids(bulk, [14001])
    print(part)


if __name__ == '__main__':
    main()
