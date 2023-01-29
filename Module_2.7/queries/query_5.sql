SELECT 
	t.name AS [Teacher],
	d.name AS [Discipline]
FROM 
	teacher AS t
INNER JOIN 
	discipline AS d ON t.id = d.teacher_id 
ORDER BY
	t.name, d.name 
	