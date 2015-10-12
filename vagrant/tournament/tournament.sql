-- Table definitions for the tournament project.

-- drop and re-create the whole database if it already exists
-- this will ensure that old tables are never used
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

-- create players table to store player info
CREATE TABLE players (
    player_id SERIAL PRIMARY KEY,
    player_name VARCHAR(70)
);

-- create matches table to store match results
CREATE TABLE matches (
    match_id SERIAL PRIMARY KEY,
    winner_id INT REFERENCES players(player_id),
    loser_id INT REFERENCES players(player_id)
);

-- create player_standings view to get current rankings based on win record
CREATE VIEW player_standings AS
    SELECT p.player_id AS player_id, p.player_name AS player_name,
    (SELECT COUNT(*) FROM matches AS m WHERE m.winner_id = p.player_id) AS wins,
    (SELECT COUNT(*) FROM matches AS m WHERE m.winner_id = p.player_id OR m.loser_id = p.player_id) AS matches
    FROM players AS p ORDER BY wins DESC;
