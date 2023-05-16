SELECT 
	s.name, 
	ROUND(AVG(m.mark_value),1) AS [Average_mark] 
FROM 
	mark AS m
INNER JOIN 
	student AS s ON m.student_id = s.id
GROUP BY 
	s.name
ORDER BY 
	AVG(m.mark_value) DESC
LIMIT 5	
	
	
	