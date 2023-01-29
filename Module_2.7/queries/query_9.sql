SELECT DISTINCT 
	s.name AS [Student],
	d.name AS [Discipline]
FROM 
	mark AS m 	
INNER JOIN 
	student AS s ON m.student_id = s.id 
INNER JOIN 
	discipline AS d ON d.id = m.discipline_id 
WHERE 
	s.name = (SELECT name FROM student LIMIT 1)