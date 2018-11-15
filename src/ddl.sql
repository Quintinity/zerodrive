set FOREIGN_KEY_CHECKS = 0;
drop table if exists Folder;
drop table if exists File;
drop table if exists Session;
drop table if exists User;
set FOREIGN_KEY_CHECKS = 1;

create table User(
    id int not null auto_increment,
    username varchar(64) not null,
    hashpw varchar(64),
    salt varchar(48),
    is_unb_account boolean not null default false,

    max_storage_space int not null,

    primary key(id),
    unique key unique_username (username, is_unb_account)
);

create table Folder(
    id int not null auto_increment,
    name varchar(128) not null,
    user_id int not null,
    parent_folder int,

    last_modified timestamp default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,

    primary key(id),
    foreign key(user_id) references User(id) on delete cascade,
    foreign key(parent_folder) references Folder(id) on delete cascade,
    unique key ensure_unique_names_in_folder (name, parent_folder)
);
alter table Folder auto_increment = 1;

create table File(
    id int not null auto_increment,
    name varchar(128) not null,
    user_id int not null,
    parent_folder int not null,

    last_modified timestamp default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
    data longblob not null,
    size_bytes int not null,

    primary key(id),
    foreign key(user_id) references User(id),
    foreign key(parent_folder) references Folder(id) on delete cascade,
    unique key ensure_unique_names_in_folder (name, parent_folder)
);

create table Session(
    token varchar(64) not null,
    user_id int not null,
    expiry_time datetime not null,

    primary key(token),
    foreign key(user_id) references User(id) on delete cascade
);
