SELECT 
	f.name AS [Faculty],
	d.name AS [Discipline],
	s.name AS [Student],
	m.mark_date,
	m.mark_value
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
ORDER BY
	f.name, s.name, m.mark_date DESC