CREATE TABLE customer(
    cid CHAR(5) PRIMARY KEY,
    name VARCHAR(30),
    bdate DATE,
    city VARCHAR(20),
    nationality VARCHAR(20)
);
CREATE TABLE account(
    aid CHAR(8) PRIMARY KEY,
    branch VARCHAR(20),
    balance FLOAT,
    openDate DATE,
    city VARCHAR(20)
);
CREATE TABLE owns(
    cid CHAR(5),
    aid CHAR(8),
    PRIMARY KEY(cid, aid),
    FOREIGN KEY (cid) REFERENCES customer(cid),
    FOREIGN KEY (aid) REFERENCES account(aid)
);
INSERT INTO customer
VALUES ('10001', 'Ayse', '1990-09-08', 'Ankara', 'TC');
INSERT INTO customer
VALUES ('10002', 'Ali', '1985-10-16', 'Ankara', 'TC');
INSERT INTO customer
VALUES ('10003', 'Ahmet', '1997-02-15', 'Izmir', 'TC');
INSERT INTO customer
VALUES ('10004', 'John', '2003-04-26', 'Istanbul', 'UK');
INSERT INTO account
VALUES (
        'A0000001',
        'Kizilay',
        40000.00,
        '2019-11-01',
        'Ankara'
    );
INSERT INTO account
VALUES (
        'A0000002',
        'Kadikoy',
        228000.00,
        '2011-01-05',
        'Istanbul'
    );
INSERT INTO account
VALUES (
        'A0000003',
        'Cankaya',
        432000.00,
        '2016-05-14',
        'Ankara'
    );
INSERT INTO account
VALUES (
        'A0000004',
        'Bilkent',
        100500.00,
        '2023-06-01',
        'Ankara'
    );
INSERT INTO account
VALUES (
        'A0000005',
        'Tandogan',
        77800.00,
        '2013-03-20',
        'Ankara'
    );
INSERT INTO account
VALUES (
        'A0000006',
        'Konak',
        25000.00,
        '2022-01-22',
        'Izmir'
    );
INSERT INTO account
VALUES (
        'A0000007',
        'Bakirkoy',
        6000.00,
        '2017-04-21',
        'Istanbul'
    );
INSERT INTO owns
VALUES ('10001', 'A0000001');
INSERT INTO owns
VALUES ('10001', 'A0000002');
INSERT INTO owns
VALUES ('10001', 'A0000003');
INSERT INTO owns
VALUES ('10001', 'A0000004');
INSERT INTO owns
VALUES ('10002', 'A0000001');
INSERT INTO owns
VALUES ('10002', 'A0000003');
INSERT INTO owns
VALUES ('10002', 'A0000005');
INSERT INTO owns
VALUES ('10003', 'A0000006');
INSERT INTO owns
VALUES ('10003', 'A0000007');
INSERT INTO owns
VALUES ('10004', 'A0000006');