SELECT
	t.name AS [Teacher],
	d.name AS [Discipline],
	ROUND(AVG(m.mark_value),1) AS [Average_mark] 
FROM 
	mark AS m
INNER JOIN
	discipline AS d ON m.discipline_id = d.id 
INNER JOIN 
	teacher AS t ON d.teacher_id = t.id 
WHERE 
	t.name = (SELECT name FROM teacher LIMIT 1)
GROUP BY
	t.name,
	d.name