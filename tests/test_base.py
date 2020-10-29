import os
import tempfile
import unittest
from .. import create_app
from ..db import init_db

class TestBase(unittest.TestCase):
    def setUp(self):
        # with open(os.path.join(os.path.dirname(__file__),
        #     'data.sql'), 'rb') as f:

        #     _data_sql = f.read().decode('utf8')
        self.app = create_app({
            'TESTING': True,
        })
        self.app_ctx = self.app.app_context()
        self.app_ctx.push()
        init_db()

    def tearDown(self):
        self.app_ctx.pop()


if __name__ == '__main__':
    unittest.main()

