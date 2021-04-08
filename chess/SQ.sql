
CREATE DATABASE IF NOT EXISTS Game_server;

use Game_server;

create table if not exists current_game(
	session int,
    fen VARCHAR(1000),
    status VARCHAR(10),
    start_time timestamp,
    last_update timestamp,
    primary key(session)
);

create table if not exists history(
    session int,
    src varchar(20),
    tar varchar(20),
    src_piece char,
    tar_piece char,
    castling bool,
    en_passant bool,
    en_passant_target_notation varchar(2),
    half_move int,
    full_move int,
    step int default 0
);
