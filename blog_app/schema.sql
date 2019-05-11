drop table if exists users;
drop table if exists posts;

create table users (
    id integer primary key autoincrement,
    name string not null,
    email string not null,
    password string not null,
    created_at datetime,
    updated_at datetime 
);

create table posts (
    id integer primary key autoincrement,
    user_id integer not null,
    title string not null,
    body text not null,
    created_at datetime,
    updated_at datetime,
    foreign key (user_id) references users (id)
);

insert into posts(user_id, title, body, created_at, updated_at) values
(1, 'title1', 'body1', datetime('now', 'localtime'), datetime('now', 'localtime')),
(1, 'title2', 'body2', datetime('now', 'localtime'), datetime('now', 'localtime')),
(1, 'title3', 'body3', datetime('now', 'localtime'), datetime('now', 'localtime')),
(1, 'title4', 'body4', datetime('now', 'localtime'), datetime('now', 'localtime')),
(1, 'title5', 'body5', datetime('now', 'localtime'), datetime('now', 'localtime'))