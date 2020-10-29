from relatome.db import get_db

class Relationship(object):
    def __init__(self,
                 id,
                 direction,
                 target,
                 qid,
                 questionid,
                 submitted):
        self.id = id
        self.direction = direction
        self.target = target
        self.qid = qid
        self.questionid = questionid
        self.submitted = submitted

    def to_dict(self):
        return {
            'id': self.id,
            'direction': self.direction,
            'target': self.target,
            'qid': self.qid,
            'questionid': self.questionid
        }

class RelationshipTargetModes(object):
    def __init__(self, direction, questionid):
        self.target_modes = {}
        self.direction = direction
        self.questionid = questionid

    def to_dict(self):
        ret =  {
            'direction': self.direction,
            'questionid': self.questionid,
            'target_modes': sorted(
                self.target_modes.items(),reverse=True)
        }
        return ret

    def add_mode(self, target, mode):
        self.target_modes[target] = mode
        


def insert(direction, target, qid, questionid, submitted=False):
    conn, db = get_db()
    db.execute("""
        INSERT INTO relationshipTable (direction, target, qid, questionid, submitted)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
        """, (direction, target, qid, questionid, submitted))
    id = db.fetchone()
    conn.commit()
    return Relationship(id=id,
                        direction=direction,
                        target=target,
                        qid=qid,
                        questionid=questionid,
                        submitted=submitted)


def update(id, target):
    conn, db = get_db()
    print('in update')
    db.execute("""
        UPDATE relationshipTable
        SET target = %s
        WHERE id = %s
        RETURNING *
        """, (target, id))

    id, direction, target, qid,\
        questionid, submitted = db.fetchone()

    conn.commit()
    return Relationship(id=id,
                        direction=direction,
                        target=target,
                        qid=qid,
                        questionid=questionid,
                        submitted=submitted)


def delete(id):
    conn, db = get_db()
    db.execute("""
        DELETE from relationshipTable
        WHERE id = %s
        RETURNING *
        """, (id,))
    id, direction, target,\
        qid, questionid, submitted = db.fetchone()
    conn.commit()
    return Relationship(id=id,
                        direction=direction,
                        target=target,
                        qid=qid,
                        questionid=questionid,
                        submitted=submitted)


def from_qid(qid):
    _, db = get_db()
    db.execute("""
        SELECT * from relationshipTable
        WHERE qid = (%s)
        ORDER BY id ASC""", (qid,))

    return [Relationship(id=id,
                         direction=direction,
                         target=target,
                         qid=qqid,
                         questionid=questionid,
                         submitted=submitted)
        for id, direction, target,
            qqid, questionid, submitted in db.fetchall()]
    

def from_id(id):
    _, db = get_db()
    db.execute("""
        SELECT * from relationshipTable
        WHERE id = (%s)
        """, (id,))

    id, direction, target,\
        qid, questionid, submitted = db.fetchone()

    return Relationship(id=id,
                        direction=direction,
                        target=target,
                        qid=qid, 
                        questionid=questionid,
                        submitted=submitted)


def delete_with_qid(qid):
    conn, db = get_db()
    db.execute("""
        DELETE from relationshipTable
        WHERE qid = %s
        RETURNING *
        """, (qid,))
    conn.commit()
    return [Relationship(id=id,
                         direction=direction,
                         target=target,
                         qid=qqid,
                         questionid=questionid,
                         submitted=submitted)
        for id, direction, target,
            qqid, questionid, submitted in db.fetchall()]
    

def get_target_modes_with_direction_and_questionid(
        direction, questionid, submitted=False, limit=3):

    _, db = get_db()
    db.execute("""
        SELECT target, COUNT(*)
        from relationshipTable
        WHERE direction = %s
        AND questionid = %s
        AND submitted = %s
        GROUP BY target
        ORDER BY COUNT(*) DESC
        LIMIT %s;
        """, (direction, questionid, submitted, limit))

    # db.execute("""
    #     SELECT target, COUNT(*)
    #     from relationshipTable
    #     GROUP BY target
    #     ORDER BY COUNT(*) DESC
    #     LIMIT %s;
    #     """, (limit,))
    modes = RelationshipTargetModes(
            direction=direction, questionid=questionid)
    print('173')
    for target, mode in db.fetchall():
        print(mode)
        modes.add_mode(target, mode)
    return modes


def get_directions_with_questionid(questionid):

    _, db = get_db()
    db.execute("""
        SELECT direction, COUNT(*)
        from relationshipTable
        WHERE questionid = %s
        GROUP BY direction
        HAVING COUNT(*) > 0;
        """, (questionid,))

    directions = db.fetchall()
    print('in get directions')
    print(directions)
    return [direction for direction, _ in directions]
