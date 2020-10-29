-- DROP TABLE IF EXISTS user;
-- DROP TABLE IF EXISTS post;

-- CREATE TABLE user (
--   id INTEGER PRIMARY KEY AUTOINCREMENT,
--   username TEXT UNIQUE NOT NULL,
--   password TEXT NOT NULL
-- );
-- 
-- CREATE TABLE post (
--   id INTEGER PRIMARY KEY AUTOINCREMENT,
--   author_id INTEGER NOT NULL,
--   created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
--   title TEXT NOT NULL,
--   body TEXT NOT NULL,
--   FOREIGN KEY (author_id) REFERENCES user (id)
-- );
DROP TABLE IF EXISTS qcardTable CASCADE;
DROP TABLE IF EXISTS relationshipTable;
DROP TABLE IF EXISTS questionTable;
DROP TABLE IF EXISTS userTable;

CREATE TABLE questionTable (
  id SERIAL PRIMARY KEY,
  question TEXT NOT NULL
);

CREATE TABLE userTable (
  id SERIAL PRIMARY KEY,
  userName TEXT,
  email TEXT,
  password_hash TEXT
);


CREATE TABLE qcardTable (
  id  SERIAL PRIMARY KEY,
  questionid INTEGER,
  userid INTEGER,
  submitted BOOLEAN,
  FOREIGN KEY (userid) REFERENCES userTable (id),
  FOREIGN KEY (questionid) REFERENCES questionTable (id)
);


CREATE TABLE relationshipTable (
  id SERIAL PRIMARY KEY,
  direction TEXT NOT NULL,
  target TEXT NOT NULL,
  qid  INTEGER,
  questionid INTEGER,
  submitted BOOLEAN,
  FOREIGN KEY (qid) REFERENCES qcardTable (id),
  FOREIGN KEY (questionid) REFERENCES questionTable (id)
);


ALTER TABLE relationshipTable ADD FOREIGN KEY (qid) REFERENCES qcardTable (id);
