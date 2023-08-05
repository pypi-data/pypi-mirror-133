import os
import unittest
from acdh_handle_pyutils.client import HandleClient

user = 'user'
pw = 'pw'

cl = HandleClient(user, pw)
cl_one = HandleClient(user, pw, hdl_prefix='21.1234/')


class TestClient(unittest.TestCase):
    """Tests for `acdh_handle_pyutils.client` module."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""
    
    def test_001(self):
        self.assertTrue(cl.url.endswith('/'))
        self.assertTrue(cl_one.url.endswith('/'))
