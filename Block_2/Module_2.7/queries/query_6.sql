SELECT 
	f.name AS [Faculty],
	s.name AS [Student]
FROM 
	student AS s
INNER JOIN 
	faculty AS f ON s.faculty_id = f.id  
ORDER BY
	f.name, s.name 