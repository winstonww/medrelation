import unittest
from ..controllers import APIController, AuthController
from .test_base import TestBase


class APIControllerTest(TestBase):
    def setUp(self):
        super(APIControllerTest, self).setUp()
        self.controller = APIController()
        self.auth = AuthController()

    # def test_add_qcard(self):
    #     res, status = self.controller.add_qcard('Heart')
    #     res, status = self.controller.get_qcards('hi')
    #     print(res)

    # def test_get_search_results(self):
    #     controller = APIController()
    #     res, status = controller.get_search_results('Heart')
    #     print(res)

    # def test_get_all_questions(self):
    #     controller = APIController()
    #     res, status = controller.get_all_questions()

    # def test_get_all_questions(self):
    #     res, status = self.controller.get_all_questions()

    def test_all(self):
        self.auth.register({
            'username': 'Winston1',
            'email': 'winstonwongww2@gmail.com',
            'password': '123',
            'reconfirm_password': '123'})

        res, _ = self.controller.get_qcards(1)
        print("Before Add QCard")
        print(res)
        res, _ = self.controller.add_qcard(2, 1)
        res, _ = self.controller.get_qcards(1)
        print("After Add QCard")
        print(res)

        res, status = self.controller.add_relationship(
                res['qcards'][0]['id'], 'Anterior', "Brain")
        res, _ = self.controller.get_qcards(1)
        print("After Add relationship")
        print(res)

        res, status = self.controller.update_relationship(
                res['qcards'][0]['relationships'][0]['id'], "Heart")
        res, _ = self.controller.get_qcards(1)
        print("After Update relationship")
        print(res)

        res, status = self.controller.add_relationship(
                res['qcards'][0]['id'], 'Anterior', "Brain")
        res, _ = self.controller.get_qcards(1)
        print("After Add relationship")
        print(res)

        res, status = self.controller.add_relationship(
                res['qcards'][0]['id'], 'Anterior', "Brain")
        res, _ = self.controller.get_qcards(1)
        print("After Add relationship")
        print(res)

        res, status = self.controller.add_relationship(
                res['qcards'][0]['id'], 'Posterior', "Brain")
        res, _ = self.controller.get_qcards(1)
        print("After Add relationship")
        print(res)

        res, _ = self.controller.\
                get_target_modes_with_questionid_and_all_directions(2)
        print(res)

        # res, _ = self.controller.get_qcards(1)
        # res, status = self.controller.delete_relationship(
        #         res['qcards'][0]['relationships'][0]['id'])
        # print(res)
        # res, _ = self.controller.get_qcards(1)
        # print("After delete relationship")
        # print(res)

        # res, status = self.controller.delete_qcard(
        #         res['qcards'][0]['id'])
        # res, _ = self.controller.get_qcards(1)
        # print("After delete qcard")
        # print(res)



if __name__ == '__main__':
    unittest.main()
