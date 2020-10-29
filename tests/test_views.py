from pathlib import Path
print('Running' if __name__ == '__main__' else 'Importing', Path(__file__).resolve())
import unittest
from ..models import QCard
from ..views import UserQCardsView

class UserQCardsViewsTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_render_single_qcard(self):
        qcards = [QCard(qid=0, question='Brain', relationships=[])]
        view = UserQCardsView()
        res, status = view.render(qcards)
        self.assertEqual({'qcards': [{
            'id': 0,
            'question': 'Brain',
            'relationships': []}]}, res)
        self.assertEqual(status, 200)


if __name__ == '__main__':
    unittest.main()

