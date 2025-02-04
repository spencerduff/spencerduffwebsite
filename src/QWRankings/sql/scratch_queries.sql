SELECT pgs.name, pgs.map, pgs.win, pgs.frags, pgws.kills_enemy, pgws.dmg_enemy, pgws.kills_team, pgws.pickups_dropped, pgs.match_user_id FROM public.per_game_per_weapon_stats pgws
INNER JOIN per_game_stats pgs
ON pgws.match_user_id_weapon = pgs.sng_stats
AND pgs.map = 'e1m2'
ORDER BY pgws.dmg_enemy DESC 

SELECT match_user_id, name, mode, win, map, ping, frags, deaths, tk, spawn_frags, dmg_given FROM per_game_stats ORDER BY frags DESC limit 25

SELECT name, win, map, ping, frags, deaths, tk, spawn_frags, dmg_given FROM per_game_stats ORDER BY deaths ASC limit 25

SELECT name, map, count(*), win FROM per_game_stats WHERE name = 'Nico' GROUP BY map, name, win

SELECT * from per_game_ratings WHERE match_id = '2024-03-19 06:29:36 +0000la.quake.world:28501 NAQW'

SELECT o3.name, o3.avg_dmg, o3.num_of_games, o3.avg_pickups, (o3.avg_dmg / o3.avg_pickups) as avg_dmg_per_pickup
FROM (
SELECT o2.name, o2.avg_dmg, o2.num_of_games, (o2.pickups_sum / o2.num_of_games) as avg_pickups FROM (
SELECT o1.name, avg(o1.dmg_enemy) as avg_dmg, count(*) as num_of_games, sum(o1.pickups_taken) as pickups_sum FROM
(SELECT pgs.name, pgws.dmg_enemy, pgws.pickups_taken FROM public.per_game_per_weapon_stats pgws
INNER JOIN per_game_stats pgs
ON pgws.match_user_id_weapon = pgs.lg_stats
AND pgs.map = 'dm3') o1
GROUP BY o1.name
ORDER BY avg_dmg DESC) o2
WHERE o2.num_of_games >= 50) o3
ORDER BY avg_dmg_per_pickup DESC

SELECT o3.name, o3.avg_dmg, o3.num_of_games, o3.avg_pickups, (o3.avg_dmg / o3.avg_pickups) as avg_dmg_per_pickup
FROM (
SELECT o2.name, o2.avg_dmg, o2.num_of_games, (o2.pickups_sum / o2.num_of_games) as avg_pickups FROM (
SELECT o1.name, avg(o1.dmg_enemy) as avg_dmg, (sum(o1.acc_hits) / sum(o1.acc_attacks)) as accuracy, count(*) as num_of_games, sum(o1.pickups_taken) as pickups_sum FROM
(SELECT pgs.name, pgws.dmg_enemy, pgws.acc_hits, pgws.acc_attacks pgws.pickups_taken FROM public.per_game_per_weapon_stats pgws
INNER JOIN per_game_stats pgs
ON pgws.match_user_id_weapon = pgs.lg_stats
AND pgs.map = 'dm3') o1
GROUP BY o1.name
ORDER BY accuracy DESC) o2
WHERE o2.num_of_games >= 50) o3
ORDER BY avg_dmg_per_pickup DESC

SELECT c1.name, c2.max_rating, c2.mode, c2.map FROM current_ratings c1 
INNER JOIN (
SELECT max(rating) as max_rating, mode, map FROM current_ratings
GROUP BY mode, map) c2
ON c1.rating = c2.max_rating AND c1.mode = c2.mode AND c1.map = c2.map  ORDER BY c2.max_rating DESC

SELECT * FROM current_ratings WHERE name = 'zorak' AND mode = '1on1' order by rating DESC

SELECT * FROM current_ratings WHERE name = 'BLooD_DoG(D_P)' AND mode = '4on4' order by rating DESC

SELECT c1.name, c1.mode, c1.map, c1.rating, c1.ratings_deviation, c2.rank_no FROM current_ratings c1
INNER JOIN (
SELECT name, mode, map, rating, ratings_deviation, RANK () OVER (
PARTITION BY map, mode
ORDER BY rating DESC
) AS rank_no FROM current_ratings) c2
ON c1.name = c2.name AND c1.mode = c2.mode AND c1.map = c2.map
WHERE c1.name = 'zorak' AND c1.map in ('aerowalk', 'ALL', 'bravado', 'dm4', 'dm6', 'dm2', 'dm3', 'skull', 'ztndm3', 'e1m2', 'zeit', 'katla', 'phantombase', 'schloss', 'shifter')
order by rating DESC


select * from current_ratings where mode = '1on1' and map = 'ALL' order by rating DESC

SELECT * FROM current_ratings WHERE name = 'bogojoker' AND mode = '4on4' order by rating DESC

SELECT * FROM current_ratings WHERE name in ('BLooD_DoG(D_P)', 'dusty', 'namtsui',
'pharm', 'enas', 'Nico', 'Schotty', 'bogojoker', 'zorak', 'coj', 'phylter', 'blaze', 'chr1s', 'Chr1s', 'Pred', 'war', 'foobar', 'yeti', 'Flynn' ) AND mode = '4on4' order by rating DESC

SELECT * FROM current_ratings WHERE name = 'blaze' AND mode = '1on1' order by rating DESC

SELECT name, map, count(*), win FROM per_game_ratings WHERE name = 'hmr' and mode = '2on2' and map = 'aerowalk' group by name, win, map