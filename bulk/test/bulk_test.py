# coding: utf-8
"""the interface for bulk_test"""

import os


def main():
    """the interface for bulk_test"""
    from bulk.bulk import Bulk

    test_path = os.path.join('..', '..', 'models')
    bdf_filename = os.path.join(test_path, 'FEM-001.bdf')

    bulk = Bulk()
    bulk.read_bulk(bdf_filename)


if __name__ == '__main__':
    main()
