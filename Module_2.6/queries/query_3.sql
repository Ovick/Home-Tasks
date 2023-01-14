SELECT 
	d.name AS [Discipline],
	f.name  AS [Faculty], 
	ROUND(AVG(m.mark_value),1) AS [Average_mark] 
FROM 
	mark AS m
INNER JOIN 
	student AS s ON m.student_id = s.id
INNER JOIN 
	faculty AS f ON s.faculty_id = f.id 
INNER JOIN 
	discipline AS d ON m.discipline_id = d.id
WHERE 
	d.name = (SELECT name FROM discipline LIMIT 1)
GROUP BY 
	f.name
ORDER BY 
	AVG(m.mark_value) DESC	