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
AND pgs.name LIKE 'TEAM:%') o1
GROUP BY o1.name
ORDER BY avg_dmg DESC) o2
WHERE o2.num_of_games >= 50) o3
ORDER BY avg_dmg_per_pickup DESC

-- Avg lg dmg per lg pickup on dm3
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

SELECT o2.name, o2.avg_dmg, o2.num_of_games, o2.accuracy FROM (
SELECT o1.name, avg(o1.dmg_enemy) as avg_dmg, (sum(o1.acc_hits) / sum(o1.acc_attacks)) as accuracy, count(*) as num_of_games, sum(o1.pickups_taken) as pickups_sum FROM
(SELECT pgs.name, pgws.dmg_enemy, pgws.acc_hits, pgws.acc_attacks, pgws.pickups_taken FROM public.per_game_per_weapon_stats pgws
INNER JOIN per_game_stats pgs
ON pgws.match_user_id_weapon = pgs.lg_stats
WHERE mode = '2on2' AND pgs.name LIKE 'TEAM:%') o1
GROUP BY o1.name
ORDER BY accuracy DESC) o2
WHERE o2.num_of_games >= 50

SELECT o2.name, o2.avg_dmg, o2.num_of_games, o2.avg_dropped_rls, (o2.pickups_sum / num_of_games) as pickups_avg,
(o2.pickups_dropped / o2.pickups_sum) as avg_drop_percent FROM (
SELECT o1.name, avg(o1.dmg_enemy) as avg_dmg, avg(o1.pickups_dropped) as avg_dropped_rls, count(*) as num_of_games,
sum(o1.pickups_total_taken) as pickups_sum, sum(o1.pickups_dropped) as pickups_dropped FROM
(SELECT pgs.name, pgws.dmg_enemy, pgws.acc_hits, pgws.acc_attacks, pgws.pickups_dropped, pgws.pickups_total_taken FROM public.per_game_per_weapon_stats pgws
INNER JOIN per_game_stats pgs
ON pgws.match_user_id_weapon = pgs.rl_stats
WHERE mode = '4on4' AND pgs.name LIKE 'TEAM:%') o1
GROUP BY o1.name) o2
WHERE o2.num_of_games >= 50
ORDER BY avg_drop_percent ASC

SELECT o2.name, o2.avg_pents, o2.num_of_games FROM
(SELECT o1.name, (CAST(sum(o1.p_took) AS DECIMAL) / (count(*))) as avg_pents, count(*) as num_of_games FROM
(SELECT pgs.name, pgis.p_took FROM public.per_game_item_stats pgis
INNER JOIN per_game_stats pgs
ON pgis.match_user_id = pgs.match_user_id
WHERE map = 'dm3' AND mode = '4on4' AND pgs.name LIKE 'TEAM:%') o1
GROUP BY o1.name) o2
WHERE o2.num_of_games > 50
ORDER BY avg_pents DESC

-- Top ranked player for every map and mode
SELECT c1.name, c2.max_rating, c2.mode, c2.map FROM current_ratings c1
INNER JOIN (
SELECT max(rating) as max_rating, mode, map FROM current_ratings
GROUP BY mode, map) c2
ON c1.rating = c2.max_rating AND c1.mode = c2.mode AND c1.map = c2.map  ORDER BY c2.max_rating DESC

SELECT * FROM current_ratings WHERE name = 'zorak' AND mode = '1on1' order by rating DESC

SELECT * FROM current_ratings WHERE name = 'BLooD_DoG(D_P)' AND mode = '4on4' order by rating DESC

-- Player and ranks on selected maps
SELECT c1.name, c1.mode, c1.map, c1.rating, c1.ratings_deviation, c2.rank_no FROM current_ratings c1
INNER JOIN (
SELECT name, mode, map, rating, ratings_deviation, RANK () OVER (
PARTITION BY map, mode
ORDER BY rating DESC
) AS rank_no FROM current_ratings) c2
ON c1.name = c2.name AND c1.mode = c2.mode AND c1.map = c2.map
WHERE c1.name = 'zorak' AND c1.map in ('aerowalk', 'ALL', 'bravado', 'dm4', 'dm6', 'dm2', 'dm3', 'skull', 'ztndm3', 'e1m2', 'zeit', 'katla', 'phantombase', 'schloss', 'shifter')
order by rating DESC

SELECT * from per_game_ratings where name = 'zorak' and map = 'bravado' and mode = '2on2'


select name, win, map, mode, count(*) as count FROM per_game_stats
where name = 'BLooD_DoG(D_P)' and mode = '1on1'
group by name, win, map, mode
ORDER BY map


select name, win, map, mode, count(*) as count FROM per_game_stats
where name = 'zorak' and mode = '1on1'
group by name, win, map, mode
ORDER BY map

-- Player head to head ratings in 1on1
SELECT pgr1.name, pgr1.win, count(*) as num_of_played FROM per_game_ratings pgr1
INNER JOIN
(SELECT * from per_game_ratings where name = 'BLooD_DoG(D_P)' and mode = '1on1') pgr2
ON pgr1.match_id = pgr2.match_id group by pgr1.name, pgr1.win
ORDER BY num_of_played DESC

SELECT * FROM current_ratings order by rating DESC



SELECT * FROM current_ratings where name LIKE 'TEAM:%' order by rating DESC

SELECT * FROM current_ratings WHERE name = 'bogojoker' AND mode = '4on4' order by rating DESC

-- Current ratings for NA 4on4 players
SELECT * FROM current_ratings WHERE name in ('BLooD_DoG(D_P)', 'dusty', 'namtsui',
'pharm', 'enas', 'Nico', 'Schotty', 'bogojoker', 'zorak', 'coj', 'phylter', 'blaze', 'chr1s', 'Chr1s', 'Pred', 'war', 'foobar', 'yeti', 'Flynn' )
AND mode = '4on4' AND map = 'ALL' order by rating DESC

SELECT name, CAST(sum(win) AS DECIMAL) / count(*)  as winrate FROM per_game_ratings WHERE name in
('bance', 'blaze', 'BLooD_DoG(D_P)', 'bogojoker', 'chr1s', 'Chr1s', 'coj', 'cronus', 'dusty',
'enas', 'Flynn', 'foobar', 'namtsui', 'Nico', 'pharm', 'phylter', 'Pred', 'Schotty', 'war', 'yeti', 'zorak'
) AND mode = '4on4' group by name order by winrate DESC


SELECT * FROM current_ratings WHERE mode = '1on1' AND map = 'ztndm3' and ratings_deviation < 150 order by rating DESC

SELECT * FROM current_ratings WHERE name = 'blaze' AND mode = '1on1' order by rating DESC

SELECT name, map, count(*), win FROM per_game_ratings WHERE name = 'hmr' and mode = '2on2' and map = 'aerowalk' group by name, win, map


-- TRUNCATE TABLE per_game_stats CASCADE;
-- TRUNCATE TABLE current_ratings CASCADE;
-- TRUNCATE TABLE per_game_item_stats CASCADE;
-- TRUNCATE TABLE per_game_per_weapon_stats CASCADE;
-- TRUNCATE TABLE per_game_ratings CASCADE;