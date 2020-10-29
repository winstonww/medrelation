from validate_email import validate_email
from .constants import DIRECTIONS
import relatome.orm.questionTable as qnt
import relatome.orm.qcardTable as qct
import relatome.orm.userTable as usert
import relatome.orm.relationshipTable as rt
from .exceptions import (
    DuplicationException,
    InvalidEntryException
)
from werkzeug.security import check_password_hash, generate_password_hash


class AuthValidator:
    def _validate_not_null(self, field):
        return field

    def _validate_reconfirm_password(self, pw, re_pw):
        return pw == re_pw

    def _validate_email(self, email):
        return validate_email(str(email))

    def validate_register(self, form):
        err = {}
        for key, val in form.items():
            if not self._validate_not_null(val):
                err[key] = "Entry is required."

        user = usert.from_username(form['username'])
        if user:
            err["username"] = "Username is taken"

        if not self._validate_reconfirm_password(
                form['password'],
                form['reconfirm_password']):
            err["reconfirm_password"] = \
                    "Password reconfirmation is incorrect"

        if not self._validate_email(form['email']):
            err['email'] = "Email address is invalid"

        if err:
            raise InvalidEntryException(err)

    def validate_login(self, form):
        err = {}
        user = usert.from_username(form['username'])
        if not user:
            err['username'] = "Username given does not exist"
            raise InvalidEntryException(err)

        if not check_password_hash(
                user.password_hash, form['password']):

            raise InvalidEntryException({
                "password": "Incorrect password"})


class UserQCardModelValidator:
    def __init__(self):
        self.directions = DIRECTIONS

    def validate_get_qcards(self, userid):
        print("in validate_get_qcards")
        print(userid)
        if not isinstance(userid, int):
            raise TypeError('Argument userid is not an int')

        user = usert.from_id(userid)
        if not user:
            raise InvalidEntryException({"userid": "Invalid user"})

    def validate_add_relationship(self, rel, target):
        err = {}
        if rel not in self.directions:
            err['rel'] = "Invalid Direction"
        if not target:
            err['target'] = "Field cannot be empty"
        elif not qnt.from_question(target):
            err['target'] = "Organ does not exist in database"
        if err:
            raise InvalidEntryException(err)

    def validate_update_relationship(self, target):
        question, err = qnt.from_question(target), {}
        if not target:
            err['target'] = "Field cannot be empty"
        elif not question:
            err['target'] = "Organ does not exist in database"
        if err:
            raise InvalidEntryException(err)

    def validate_delete_relationship(self, rid):
        relationship, err = rt.from_id(rid), {}
        if not rid:
            err['id'] = "ID cannot be empty"
        elif not relationship:
            err['id'] = "Relationship does not exist"
        if err:
            raise InvalidEntryException(err)


    def validate_add_qcard(self, questionid, userid):
        if not isinstance(userid, int):
            raise TypeError('Argument userid is not an int')
        user = usert.from_id(userid)
        question = qnt.from_id(questionid)
        print('in validate_add_qcard')
        print(userid)
        print(user)
        if not user:
            raise InvalidEntryException({"userid": "Invalid user"})

        if not question:
            raise InvalidEntryException({"questionid": "Invalid question id"})

        existing = qct.from_questionid_and_userid(questionid, userid)
        if existing is not None:
            raise DuplicationException(
                {existing.question.question: "Card already exists in deck."})

    def validate_delete_qcard(self, qid):
        qcard = qct.from_id(qid)
        if not qcard:
            raise InvalidEntryException({"id": "Invalid QCard"})
