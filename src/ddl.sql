drop table if exists Item;
drop table if exists User;

create table User(
    id int not null auto_increment,
    username varchar(50) not null,
    hashed_password varchar(64) not null,
    salt varchar(48) not null,

    primary key(id)
);

create table Item(
    id int not null auto_increment,
    name varchar(25) not null,
    data blob,
    size_bytes int,
    last_modified datetime,
    is_directory boolean default false,
    parent int,
    user_id int not null,
    
    primary key(id),
    foreign key(user_id) references User(id) on delete cascade,
	foreign key(parent) references Item(id) on delete cascade
);
