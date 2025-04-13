-- найти сведения обо всех расходах, выполненных по конкретному направлению в текущем году (направление расходов – параметр запроса)
select o.*
from operation o
         join opration_type ot using (operation_type_id)
where ot.name = :type
  and extract(year from o.operation_date) = extract(year from now());

-- найти сведения обо всех доходных и расходных операциях с отрицательной суммой
select ot.is_income, ot.name, o.*
from operation o
         left join opration_type ot using (operation_type_id)
where o.amount < 0;

-- найти сведения о пяти статьях расходов, по которым были выполнены самые большие суммарные расходы в текущем году. Отсортировать результат запроса по убыванию этих сумм.
select ot.name, abs(sum(o.amount)) as total_expencese
from operation o
         join opration_type ot using (operation_type_id)
where ot.is_income = false
  and extract(year from o.operation_date) = extract(year from now())
  and o.amount < 0
group by ot.operation_type_id
order by 2 desc
limit 5;