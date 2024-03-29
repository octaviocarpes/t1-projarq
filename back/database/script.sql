PRAGMA foreign_keys = ON;

CREATE TABLE STUDENT (
    username VARCHAR(50) PRIMARY KEY,
    password VARCHAR(20) NOT NULL,
    course VARCHAR (2) NOT NULL
);

CREATE TABLE TEAM (
    team_name VARCHAR(50) PRIMARY KEY,
    admin VARCHAR(50) NOT NULL,
    rate REAL NOT NULL,
    FOREIGN KEY (admin) REFERENCES STUDENT(username)
);

CREATE TABLE STUDENT_TEAM (
    team_name VARCHAR (50) NOT NULL,
    username VARCHAR (50) NOT NULL UNIQUE,
    FOREIGN KEY (team_name) REFERENCES TEAM(team_name),
    FOREIGN KEY (username) REFERENCES STUDENT(username),
    PRIMARY KEY (team_name, username)
);

CREATE TABLE CERTIFICATE (
    certificate_id INTEGER PRIMARY KEY,
    username VARCHAR (50) NOT NULL,
    team_name VARCHAR (50) NOT NULL,
    generation_date VARCHAR (15) NOT NULL,
    FOREIGN KEY (team_name) REFERENCES TEAM(team_name)
);

CREATE TABLE VALUER (
    username VARCHAR(50) PRIMARY KEY,
    password VARCHAR (20) NOT NULL
);