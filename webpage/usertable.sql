#Used https://flask.palletsprojects.com/en/1.1.x/tutorial/database/, flask tutorial for making a database
CREATE TABLE user (
  id TEXT PRIMARY KEY,
  profile_pic TEXT NOT NULL,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL
);