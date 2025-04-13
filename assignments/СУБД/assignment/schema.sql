create table if not exists family
(
	family_id serial
		constraint family_pk
			primary key,
	family_name varchar(64) not null
);

alter table family owner to postgres;

create unique index if not exists family_family_id_uindex
	on family (family_id);

create table if not exists currency
(
	currency_id serial
		constraint currency_pk
			primary key,
	name varchar(64) not null,
	symbol varchar(16) not null,
	rate_to_base_currency double precision not null,
	decimal_numbers integer not null
		constraint valid_decimal_number_check
			check (decimal_numbers >= 0)
);

alter table currency owner to postgres;

create unique index if not exists currency_currency_id_uindex
	on currency (currency_id);

create unique index if not exists currency_name_uindex
	on currency (name);

create table if not exists "user"
(
	user_id serial
		constraint user_pk
			primary key,
	first_name varchar(64) not null,
	last_name varchar(64) not null,
	register_date timestamp default now() not null,
	family_id integer not null
		constraint user_family_family_id_fk
			references family
);

alter table "user" owner to postgres;

create unique index if not exists user_user_id_uindex
	on "user" (user_id);

create table if not exists opration_type
(
	operation_type_id serial
		constraint opration_type_pk
			primary key,
	name varchar(128) not null,
	is_income boolean not null
);

alter table opration_type owner to postgres;

create unique index if not exists opration_type_operation_type_id_uindex
	on opration_type (operation_type_id);

create unique index if not exists opration_type_name_uindex
	on opration_type (name);

create table if not exists operation
(
	operation_id serial
		constraint operation_pk
			primary key,
	operation_date timestamp default now() not null,
	modify_date timestamp default now() not null,
	description varchar(256),
	is_cash boolean not null,
	amount numeric(30,15) default 0 not null,
	currency_id integer not null
		constraint operation_currency_currency_id_fk
			references currency,
	user_id integer not null
		constraint operation_user_user_id_fk
			references "user",
	operation_type_id integer
);

alter table operation owner to postgres;

create unique index if not exists operation_operation_id_uindex
	on operation (operation_id);

