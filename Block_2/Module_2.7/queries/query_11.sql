SELECT 
	t.name AS [Teacher],
	s.name AS [Student],
	ROUND(AVG(m.mark_value),1) AS [Average_mark] 
FROM 
	mark AS m 	
INNER JOIN 
	student AS s ON m.student_id = s.id 
INNER JOIN 
	discipline AS d ON d.id = m.discipline_id
INNER JOIN 
	teacher AS t ON d.teacher_id = t.id  
WHERE 
	s.name = (SELECT name FROM student LIMIT 1)
	AND t.name = (SELECT name FROM teacher LIMIT 1)
GROUP BY
	t.name, s.name 