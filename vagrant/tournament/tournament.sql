-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

CREATE TABLE players (
    player_id SERIAL PRIMARY KEY,
    player_name VARCHAR(70)
);

CREATE TABLE matches (
    match_id SERIAL PRIMARY KEY,
    winner_id INT REFERENCES players(player_id),
    loser_id INT REFERENCES players(player_id)
);

CREATE VIEW player_standings AS
    SELECT p.player_id AS player_id, p.player_name AS player_name,
    (SELECT COUNT(*) FROM matches AS m WHERE m.winner_id = p.player_id) AS wins,
    (SELECT COUNT(*) FROM matches AS m WHERE m.winner_id = p.player_id OR m.loser_id = p.player_id) AS matches
    FROM players AS p ORDER BY wins DESC;
