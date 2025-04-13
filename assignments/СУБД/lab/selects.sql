--Выбирите СУБД Oracle для выполнения лабораторной.
--Cкопируйте файл EDU1.sql в каталог C:\TEMP .
--Раскройте файл и ознакомтесь со скриптом создания и заполнения таблиц для выполнения лабораторной.
--Произведите запуск SQLPlus. или PLSQLDeveloper. или другого инструментария Oracle и соеденитесь с БД. Запустите скрипт EDU1.sql на выполнение.
--Вставте в эту строку Ваши ФИО, номер группы, курса. ФИО , группа , курс .
--Файл с отчётом о выполнении лабораторной создаётся путём вставки соответсвующего select-предложения после строки с текстом задания.
--Файл отчёта именуется фамилией студента в английской транскрипции, с расширением .txt и отправте в систему edufpmi как ответ к заданию.
--НЕ ДОПУСКАЕТСЯ ИЗМЕНЕНИЕ ТЕКСТОВ ЗАДАНИЙ И ОТПРАВКА ВЫПОЛНЕННОЙ РАБОТЫ В ФАЙЛЕ ДРУГОГО ФОРМАТА!!!
--Тексты заданий:
--1.	Выдать информацию об адресе отдела продаж (Sales) компании.
SELECT D.DEPTADDRESS
FROM DEPT D
WHERE D.DEPTNAME = 'Sales';

--2.	Выдать информацию обо всех работниках, родившихся не ранее 1 января 1985 года.
SELECT E.*
FROM EMP e
WHERE E.BIRTHDATE >= DATE '1985-01-01';

--3.	Найти минимальный оклад, предусмотренный для водителя  (Driver).
SELECT J.MINSALARY
FROM JOB J
WHERE J.JOBNAME = 'Driver';

--4.	Подсчитать число работников, работавших в компании после  31 мая 2017 года хотя бы один день (31 мая 2017 года не включается).
SELECT COUNT(DISTINCT C.EMPNO)
FROM CAREER C
WHERE c.STARTDATE > date '2017-05-31'
  and (c.STARTDATE < COALESCE(c.ENDDATE, TRUNC(CURRENT_DATE)));

--5.	Найти минимальные премии, начисленные в 2016, 2017, 2018, 2019? 2020 годах (указать год и минимальную. премию в хронологическом порядке).
SELECT B.YEAR, min(B.BONVALUE)
FROM BONUS B
WHERE B.YEAR BETWEEN 2016 AND 2020
GROUP BY B.YEAR
ORDER BY 1;

--6.	Выдать информацию о кодах всех должностей,  на которых работала работник Nina Tihanovich. Если Nina Tihanovich работает в настоящее время -
--должность также включается в искомый список.
SELECT DISTINCT(J.JOBNO)
FROM EMP E
         JOIN CAREER C ON E.EMPNO = C.EMPNO
         JOIN JOB J on C.JOBNO = J.JOBNO
WHERE E.EMPNAME = 'Nina Tihanovich';

--7.	Выдать информацию о названиях должностей,  на которых работали работники Richard Martin и Jon Martin. Если один из них или оба  работают в настоящее время -
--должность также включается в искомый список. Должность выдаётся вместе с ФИО (empname) работника.
SELECT DISTINCT E.EMPNAME, J.JOBNAME
FROM EMP E
         JOIN CAREER C on E.EMPNO = C.EMPNO
         JOIN JOB J on C.JOBNO = J.JOBNO
WHERE E.EMPNAME IN ('Richard Martin', 'Jon Martin');


-- 8.	Найти фамилии, коды должностей и периоды работы (даты приема и даты увольнения) для всех клерков (Clerk) и водителей (Driver),
--работавших или работающих в компании. Для работающих дата увольнения для периода неопределена и при выводе либо отсутсвует, либо определяется как Null.
SELECT E.EMPNAME, J.JOBNO, C.STARTDATE, C.ENDDATE
FROM JOB J
         JOIN CAREER C ON J.JOBNO = C.JOBNO
         JOIN EMP E on C.EMPNO = E.EMPNO
WHERE J.JOBNAME IN ('Clerk', 'Driver');

-- 9.	Найти фамилии, названия должностей и периоды работы (даты приема и даты увольнения) для бухгалтеров (Accountant) и исполнительных директоров (Executive Director),
--работавших или работающих в компании. Для работающих дата увольнения для периода неопределена и при выводе либо отсутсвует, либо определяется как Null.
SELECT E.EMPNAME, J.JOBNAME, C.STARTDATE, C.ENDDATE
FROM EMP E
         JOIN CAREER C ON E.EMPNO = C.EMPNO
         JOIN JOB J on C.JOBNO = J.JOBNO
WHERE J.JOBNAME IN ('Accountant', 'Executive Director');

-- 10.	Найти количество различных работников, работавших в отделе B02 в период с 01.01.2014 по 31.12.2017 хотя бы один день.
SELECT COUNT(DISTINCT C.EMPNO)
FROM CAREER C
WHERE C.DEPTID = 'B02'
  AND C.STARTDATE >= DATE '2014-01-01'
  AND C.ENDDATE <= DATE '2017-12-31'
  AND C.ENDDATE > C.STARTDATE;

-- 11.	Найти фамилии этих работников.
SELECT DISTINCT E.EMPNAME
FROM CAREER C
         JOIN EMP E ON C.EMPNO = E.EMPNO
WHERE C.DEPTID = 'B02'
  AND C.STARTDATE >= DATE '2014-01-01'
  AND C.ENDDATE <= DATE '2017-12-31'
  AND C.ENDDATE > C.STARTDATE;

--12.	Найти номера и названия отделов, в которых не было ни одного работника в период с 01.01.2015 по 31.12.2015.
SELECT D.DEPTID, D.DEPTNAME
FROM DEPT D
WHERE NOT EXISTS(
        SELECT 1
        FROM CAREER C
        WHERE C.DEPTID = D.DEPTID
          AND NOT (C.STARTDATE > DATE '2015-12-31'
            OR C.ENDDATE < DATE '2015-01-01'
            ));

--13.	Найти информацию о работниках (номер, фамилия), для которых нет начислений премии в период с 01.01. 2016 по  31.12.2017.
SELECT E.EMPNO, E.EMPNAME
FROM EMP E
WHERE NOT EXISTS(
        SELECT 1
        FROM BONUS B
        WHERE B.EMPNO = E.EMPNO
          AND B.YEAR BETWEEN 2016 AND 2017
    );

--14.	Найти количество работников, никогда не работавших  ни в исследовательском  (Research) отделе, ни в отделе поддержки (Support).
SELECT COUNT(E.EMPNO)
FROM EMP E
WHERE NOT EXISTS(
        SELECT 1
        FROM CAREER C
                 JOIN DEPT D on C.DEPTID = D.DEPTID
        WHERE C.EMPNO = E.EMPNO
          AND D.DEPTNAME IN ('Research', 'Support')
    );

-- 15.	Найти коды и фамилии работников, работавших в двух и более отделах. Если работник работает в настоящее время, то отдел также учитывается.
SELECT E.EMPNO, E.EMPNAME
FROM EMP E
         JOIN CAREER C2 on E.EMPNO = C2.EMPNO
         JOIN DEPT D on C2.DEPTID = D.DEPTID
GROUP BY E.EMPNO, E.EMPNAME
HAVING COUNT(DISTINCT D.DEPTID) >= 2;

-- 16.	Найти коды и фамилии работников, работавших на двух и более должностях. Если работник работает в настоящее время, то должность также учитывается.
SELECT E.EMPNO, E.EMPNAME
FROM EMP E
         JOIN CAREER C2 on E.EMPNO = C2.EMPNO
         JOIN JOB J on C2.JOBNO = J.JOBNO
GROUP BY E.EMPNO, E.EMPNAME
HAVING COUNT(DISTINCT J.JOBNO) >= 2;

-- 17.	Найти коды  и фамилии работников, суммарный стаж работы которых в компании не менее 4 лет.
SELECT E.EMPNO, E.EMPNAME
FROM EMP E
         JOIN CAREER C2 on E.EMPNO = C2.EMPNO
GROUP BY E.EMPNO, E.EMPNAME
HAVING SUM(COALESCE(C2.ENDDATE, TRUNC(CURRENT_DATE)) - C2.STARTDATE) >= 4 * 365;

-- 18.	Найти всех работников (коды и фамилии), увольнявшихся хотя бы один раз.
SELECT E.EMPNO, E.EMPNAME
FROM EMP E
WHERE EXISTS(
              SELECT 1
              FROM CAREER C
              WHERE C.EMPNO = E.EMPNO
                AND C.ENDDATE IS NOT NULL
          );

--19.	Найти среднии премии, начисленные за период в два 2016, 2017 года, и за период в три 2017, 2018, 2019 года, в разрезе работников
--(т.е. для работников, имевших начисления хотя бы в одном месяце двугодичного периода). Вывести id, имя и фимилию работника, период, среднюю премию.
WITH PERIODS AS (
    SELECT 2016 START_YEAR, 2017 END_YEAR
    FROM DUAL
    UNION
    SELECT 2017 START_YEAR, 2019 END_YEAR
    FROM DUAL
)
SELECT E.EMPNO, E.EMPNAME, P.START_YEAR, P.END_YEAR, COALESCE(AVG(B.BONVALUE), 0)
FROM PERIODS P
         CROSS JOIN EMP E
         LEFT JOIN BONUS B ON E.EMPNO = B.EMPNO AND B.YEAR BETWEEN P.START_YEAR AND P.END_YEAR
GROUP BY E.EMPNO, E.EMPNAME, P.START_YEAR, P.END_YEAR
ORDER BY EMPNO, START_YEAR;

--20.	Найти отделы (id, название, адрес), в которых есть начисления премий в феврале 2017 года.
SELECT D.DEPTID, D.DEPTNAME, D.DEPTADDRESS
FROM DEPT D
         JOIN CAREER C2 on D.DEPTID = C2.DEPTID
         JOIN BONUS B on C2.EMPNO = B.EMPNO
WHERE B.YEAR = 2017
  AND B.MONTH = 2
GROUP BY D.DEPTID, D.DEPTNAME, D.DEPTADDRESS;
