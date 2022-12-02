# coding: utf-8
from unittest import TestCase
import os

from pyNastran.bdf.bdf import BDF
from bulk.bulk import Part2D


class TestPart2D(TestCase):
    def setUp(self):
        # define test model
        test_path = os.path.join('..', '..', 'models', 'FEM-001')
        bdf_filename = os.path.join(test_path, 'FEM-001-full-run.bdf')
        # create instance of BDF
        self.model = BDF()
        self.model.read_bdf(bdf_filename)
        # create an instance of part2D
        part_2d_id = 13
        eids = [13001 + i for i in range(50)]
        self.part_2d = Part2D(part_2d_id,
                              {elm.eid: elm for elm in self.model.elements.values() if elm.eid in eids},
                              self.model)


class TestGetNodes(TestPart2D):
    def test_is_nodes_dict(self):
        self.assertIsInstance(self.part_2d.nodes, dict)

    def test_number_of_nodes(self):
        self.assertEqual(len(self.part_2d.nodes), 66)
