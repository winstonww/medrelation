from relatome.db import get_db


class Question(object):
    def __init__(self, id, question):
        self.id = id
        self.question = question

    def to_dict(self):
        res = {}
        res['id'] = self.id
        res['question'] = self.question
        return res
    
    def __repr__(self):
        return self.question


def all():
    _, db = get_db()
    db.execute("""
        SELECT * FROM questionTable
        """)
    return [Question(id=e[0], question=e[1])
            for e in db.fetchall()]


def from_question(question):
    '''
        return list of question objects matching question
    '''
    _, db = get_db()
    db.execute("""
        SELECT * from questionTable
        WHERE question = (%s)
        """,
        (question,))
    entries = db.fetchone()

    if not entries:
        return None

    return Question(id=entries[0],
            question=entries[1])

def from_id(id):
    '''
        return list of question objects matching question
    '''
    _, db = get_db()
    db.execute("""
        SELECT * from questionTable
        WHERE id = %s
        """,
        (id,))
    entries = db.fetchone()

    if not entries:
        return None

    return Question(id=entries[0],
            question=entries[1])
