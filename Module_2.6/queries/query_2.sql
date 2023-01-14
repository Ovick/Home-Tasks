SELECT 
	d.name AS [Discipline],
	s.name AS [Student], 
	ROUND(AVG(m.mark_value),1) AS [Average_mark] 
FROM 
	mark AS m
INNER JOIN 
	student AS s ON m.student_id = s.id
INNER JOIN 
	discipline AS d ON m.discipline_id = d.id
WHERE 
	d.name = (SELECT name FROM discipline LIMIT 1)
GROUP BY 
	s.name
ORDER BY 
	AVG(m.mark_value) DESC
LIMIT 1	