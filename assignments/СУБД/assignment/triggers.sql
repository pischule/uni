-- триггеры
-- у нас нет дат рождения, так что добавим их
alter table "user"
    add birth_date date default now() not null;
insert into public.user (birth_date)
values ('1996-02-01'),
       ('1997-07-16'),
       ('1996-03-08'),
       ('2001-10-05'),
       ('1995-12-21'),
       ('2000-08-20'),
       ('1996-09-27'),
       ('2001-12-11'),
       ('2004-02-24'),
       ('2004-05-26'),
       ('2004-12-19'),
       ('2005-05-24'),
       ('2008-03-03'),
       ('2009-03-24'),
       ('2006-05-28');
alter table "user"
    alter column birth_date drop default;

-- sequence fix
-- SELECT setval('user_user_id_seq', max(user_id)) FROM "user";

-- 1. Триггер должен запрещать членам семьи, не достигшим 16-летнего возраста,
-- совершать расходные операции на сумму более 10 рублей;

create or replace function operation_user_birth_date()
    returns trigger as
$$
declare
    min_age   int := tg_argv[0]::int;
    max_spend int := tg_argv[1]::int;
begin
    if ((select birth_date from "user" u where user_id = new.user_id) > (now() - min_age * interval '1 year')) and
       ((select (-1) * c.rate_to_base_currency * new.amount from currency c where c.currency_id = new.currency_id) >
        max_spend)
    then
        raise exception 'You''re too young!';
    end if;
    return new;
end
$$ language plpgsql;

drop trigger if exists verify_operation_amount_and_user_birth_date on public.operation;
create trigger verify_operation_amount_and_user_birth_date
    before insert or update
    on operation
    for each row
execute procedure operation_user_birth_date('16', '10');

-- example
-- select user_id,
--        case when birth_date > (now()::date - interval '16 years') then 'kid' else 'adult' end
-- from "user";
-- insert into public.operation (operation_id, operation_date, modify_date, description, is_cash, amount, currency_id, user_id, operation_type_id)
-- values (nextval('operation_operation_id_seq'), now(), now(), null, true, -30.0, 2, 15, null);
-- insert into public.operation (operation_id, operation_date, modify_date, description, is_cash, amount, currency_id, user_id, operation_type_id)
-- values (nextval('operation_operation_id_seq'), now(), now(), null, true, 30.0, 2, 15, null);

-- 2. Триггер должен запрещать проведение расходных операций всех членов семьи в месяц на сумму большую,
-- чем полученный всеми членами в месяц доходах;

create or replace function operation_family_month_budget()
    returns trigger as
$$
begin
    if (select coalesce(sum(o.amount), 0)
        from operation o
                 join "user" u using (user_id)
                 join family f using (family_id)
        where date_trunc('month', o.operation_date) = date_trunc('month', now())) + new.amount < 0
    then
        raise exception 'You have no money ((';
    end if;
    return new;
end
$$ language plpgsql;

drop trigger if exists verify_operation_family_month_budget on public.operation;
create trigger verify_operation_family_month_budget
    before insert or update
    on operation
    for each row
execute procedure operation_family_month_budget();

-- example
-- insert into public.operation (operation_id, operation_date, modify_date, description, is_cash, amount, currency_id, user_id, operation_type_id)
-- values (nextval('operation_operation_id_seq'), now(), now(), null, true, -400000000000.0, 2, 11, null);

-- 3. Триггер должен отслеживать, чтобы в течение года состав семьи изменялся не более чем на одного члена.
create or replace function family_user_count_changes()
    returns trigger as
$$
begin
    if (select count(1)
        from (
                 select u.register_date
                 from "user" u
                 where u.family_id = new.family_id
                   and u.user_id != new.user_id
                 union all
                 select new.register_date
             ) as family_users
        where family_users.register_date between
                  (now()::date - interval '1 year') and (now()::date + interval '1 year')
       ) > 1
    then
        raise exception 'Family members count can''t change more than once per year';
    end if;
    return new;
end
$$ language plpgsql;

drop trigger if exists verify_family_user_count_changes on public."user";
create trigger verify_family_user_count_changes
    before insert or update
    on "user"
    for each row
execute procedure family_user_count_changes();

-- example
-- INSERT INTO public."user"
-- VALUES (DEFAULT, 'Лола', 'Сидорова', '2021-09-20 20:46:25.526689', 5, '2006-05-28');