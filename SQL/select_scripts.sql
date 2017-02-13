#SELECT per.name, COUNT(per.name) AS NumberOfRoles
#FROM mal_project.person per, mal_project.voicerole vr
#WHERE per.id = vr.idPerson
#GROUP BY per.name

SELECT distinctRoles.name, COUNT(distinctRoles.name) AS NumberOfRoles
FROM (
	SELECT DISTINCT ani.title, per.name
	FROM mal_project.anime ani, mal_project.character cha, mal_project.voicerole vr, mal_project.person per
	WHERE ani.id=cha.idAnime AND cha.id=vr.idCharacter AND vr.idPerson=per.id
    ) AS distinctRoles
GROUP BY distinctRoles.name

/*
SELECT ani.title, stu.name
FROM mal_project.anime ani, mal_project.animestudio anistu, mal_project.studio stu
WHERE ani.id = anistu.idanime AND stu.id = anistu.idstudio;
*/

/*
SELECT c.name, p.name, v.language
FROM mal_project.character c, mal_project.person p, mal_project.voicerole v
WHERE c.id = v.idCharacter AND p.id =  v.idPerson;
*/

/*
SELECT c.name, pv.name, pv.language
FROM mal_project.character c
JOIN 
	(SELECT p.name, v.language, v.idCharacter
	FROM mal_project.person p
    JOIN mal_project.voicerole v
    ON p.id = v.idPerson) AS pv
ON c.id = pv.idCharacter
*/

/*
SELECT ani.title, COUNT(ani.title) AS titleCount
FROM mal_project.anime ani, mal_project.animestudio anistu, mal_project.studio stu
WHERE ani.id = anistu.idanime AND stu.id = anistu.idstudio
GROUP BY ani.title;
*/