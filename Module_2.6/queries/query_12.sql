SELECT 
	f.name AS [Faculty],
	d.name AS [Discipline],
	s.name AS [Student],
	m.mark_value,
	m.mark_date 
FROM 
	mark AS m 	
INNER JOIN 
	student AS s ON m.student_id = s.id 
INNER JOIN 
	faculty AS f ON s.faculty_id = f.id
INNER JOIN 
	discipline AS d ON d.id = m.discipline_id 
WHERE 
	f.name = (SELECT name FROM faculty LIMIT 1)
	AND d.name = (SELECT name FROM discipline LIMIT 1)
	AND m.mark_date = (
		SELECT MAX(m2.mark_date)
		FROM 
			mark AS m2 
		INNER JOIN 
			student AS s2 ON m2.student_id = s2.id 
		INNER JOIN 
			faculty AS f2 ON s2.faculty_id = f2.id
		WHERE 
			m2.discipline_id = m.discipline_id
			AND f2.id = f.id  
	)
	