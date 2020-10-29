from relatome.db import get_db
import relatome.orm.relationshipTable as rt
import relatome.orm.questionTable as qnt


class QCard(object):

    def __init__(self, id, questionid, userid):
        self.id = id
        self.questionid = questionid
        self.question = qnt.from_id(questionid)
        self.relationships = rt.from_qid(id)
        self.userid = userid

    def __repr__(self):
        return self.question.question

    def to_dict(self):
        res = {}
        res['id'] = self.id
        res['question'] = self.question.question
        res['questionid'] = self.questionid
        res['relationships'] = [
            rel.to_dict()
            for rel in self.relationships
        ]
        return res


def from_userid(userid):
    # [TODO]: get qcard based on user
    _, db = get_db()
    db.execute("""
        SELECT * FROM qcardTable
        WHERE userid = (%s)
        """,
        (userid,))
    qcards = db.fetchall()
    return [QCard(id=card[0],
                  questionid=card[1],
                  userid=card[2]) for card in qcards]


def from_id(id):
    _, db = get_db()
    db.execute("""
        SELECT * from qcardTable
        WHERE id = (%s)
        ORDER BY id ASC
        """,
        (id,))
    card = db.fetchone()
    if not card:
        return None
    return QCard(id=card[0],
                 questionid=card[1],
                 userid=card[2])


def from_questionid_and_userid(questionid, userid):
    _, db = get_db()
    db.execute("""
        SELECT * from qcardTable
        WHERE questionid = %s
        AND userid = %s
        """,
        (questionid, userid))
    card = db.fetchone()

    if not card:
        return None

    return QCard(id=card[0],
                 questionid=card[1],
                 userid=card[2])


def insert(questionid, userid):
    conn, db = get_db()
    db.execute("""
      INSERT INTO qcardTable (questionid, userid)
      VALUES (%s, %s)
      RETURNING *
      """,
      (questionid, userid))
    qcard = db.fetchone()
    conn.commit()
    return QCard(id=qcard[0],
                 questionid=qcard[1],
                 userid=qcard[2])

def delete(id):
    conn, db = get_db()
    db.execute("""
        DELETE from qcardTable
        WHERE id = %s
        RETURNING *
        """, (id,))
    conn.commit()
    qcard = db.fetchone()
    if not qcard:
        return None
    return QCard(id=qcard[0],
                 questionid=qcard[1],
                 userid=qcard[2])
