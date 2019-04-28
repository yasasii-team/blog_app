drop table if exists users;
drop table if exists posts;

create table users (
    id integer primary key autoincrement,
    name string not null,
    email string not null,
    password string not null,
    created_at datetime,
    update_at datetime 
);

create table posts (
    id integer primary key autoincrement,
    user_id integer not null,
    title string not null,
    body text not null,
    foreign key (user_id) references users (id)
);