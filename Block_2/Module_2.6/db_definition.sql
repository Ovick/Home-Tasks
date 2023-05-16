-- Table: faculty
DROP TABLE IF EXISTS faculty;
CREATE TABLE faculty (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) UNIQUE NOT NULL
);

-- Table: student
DROP TABLE IF EXISTS student;
CREATE TABLE student (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) UNIQUE NOT NULL,
	faculty_id INTEGER,
	FOREIGN KEY (faculty_id) REFERENCES faculty (id)
		ON UPDATE CASCADE
		ON DELETE SET NULL
);

-- Table: teacher
DROP TABLE IF EXISTS teacher;
CREATE TABLE teacher (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) UNIQUE NOT NULL
);

-- Table: discipline
DROP TABLE IF EXISTS discipline;
CREATE TABLE discipline (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) UNIQUE NOT NULL,
	teacher_id INTEGER,
	FOREIGN KEY (teacher_id) REFERENCES teacher (id)
		ON UPDATE CASCADE
		ON DELETE SET NULL
);

-- Table: mark
DROP TABLE IF EXISTS mark;
CREATE TABLE mark (
    mark_value TINYINT NOT NULL,
	mark_date DATE NOT NULL,
	student_id INTEGER NOT NULL,
    discipline_id INTEGER NOT NULL,
    PRIMARY KEY (student_id, discipline_id, mark_date)
    FOREIGN KEY (student_id) REFERENCES student(id)
        ON DELETE CASCADE 
    FOREIGN KEY (discipline_id) REFERENCES discipline(id)
        ON DELETE NO ACTION    
);