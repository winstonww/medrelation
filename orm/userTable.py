from relatome.db import get_db
class User:
    def __init__(self, id, username, email, password_hash):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash

    def to_dict(self):
        return {'id': self.id,
                'username': self.username,
                'email': self.email,
                'password_hash': self.password_hash}

    def __repr__(self):
        return self.username


def insert(username, email, password_hash):
    conn, db = get_db()
    print('in insert')
    print(username)
    print(email)
    print(password_hash)
    db.execute("""
      INSERT INTO userTable (username, email, password_hash)
      VALUES (%s, %s, %s)
      RETURNING *
      """,
      (username,email,password_hash))
    id, username, email, password_hash = db.fetchone()
    conn.commit()
    return User(id=id,
                username=username,
                email=email,
                password_hash=password_hash)

def from_username(username):
    _, db = get_db()
    db.execute("""
        SELECT * from userTable
        WHERE username = (%s)
        ORDER BY id ASC
        """,
        (username,))

    user = db.fetchone()
    if not user:
        return None

    id, username, email, password_hash = user
    return User(id=id,
                username=username,
                email=email,
                password_hash=password_hash)


def from_id(userid):
    _, db = get_db()
    db.execute("""
        SELECT * from userTable
        WHERE id = (%s)
        """,
        (userid,))

    user = db.fetchone()
    if not user:
        return None

    id, username, email, password_hash = user
    return User(id=id,
                username=username,
                email=email,
                password_hash=password_hash)


