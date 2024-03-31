CREATE TABLE customer(
     cid CHAR(5) PRIMARY KEY,
     name VARCHAR(30) NOT NULL,
     bdate DATE NOT NULL,
     city VARCHAR(20) NOT NULL,
     nationality VARCHAR(20) NOT NULL
);
CREATE TABLE account(
     aid CHAR(8) PRIMARY KEY,
     branch VARCHAR(20) NOT NULL,
     balance FLOAT NOT NULL,
     openDate DATE NOT NULL,
     city VARCHAR(20) NOT NULL
);
CREATE TABLE owns(
     cid CHAR(5) PRIMARY KEY,
     aid CHAR(8) PRIMARY KEY,
     FOREIGN KEY (cid) REFERENCES customer(cid),
     FOREIGN KEY (aid) REFERENCES account(aid)
);
INSERT INTO customer (cid, name, bdate, city, nationality)
VALUES ('10001', 'Ayse', '1990-08-09', 'Ankara', 'TC'),
     ('10002', 'Ali', '1985-10-16', 'Ankara', 'TC'),
     ('10003', 'Ahmet', '1997-02-15', 'İzmir', 'TC'),
     ('10004', 'John', '2003-04-26', 'İstanbul', 'UK');
INSERT INTO account (aid, branch, balance, openDate, city)
VALUES (
          'A0000001',
          'Kızılay',
          40000.00,
          '2019-11-01',
          'Ankara'
     ),
     (
          'A0000002',
          'Kadıköy',
          228000.00,
          '2011-01-05',
          'İstanbul'
     ),
     (
          'A0000003',
          'Çankaya',
          432000.00,
          '2016-05-14',
          'Ankara'
     ),
     (
          'A0000004',
          'Bilkent',
          100500.00,
          '2023-06-01',
          'Ankara'
     ),
     (
          'A0000005',
          'Tandogan',
          77800.00,
          '2013-03-20',
          'Ankara'
     ),
     (
          'A0000006',
          'Konak',
          25000.00,
          '2022-01-22',
          'İzmir'
     ),
     (
          'A0000007',
          'Bakırköy',
          6000.00,
          '2017-04-21',
          'İstanbul'
     );
INSERT INTO owns (cid, aid)
VALUES ('10001', 'A0000001'),
     ('10001', 'A0000002'),
     ('10001', 'A0000003'),
     ('10001', 'A0000004'),
     ('10002', 'A0000001'),
     ('10002', 'A0000003'),
     ('10002', 'A0000005'),
     ('10003', 'A0000006'),
     ('10003', 'A0000007'),
     ('10004', 'A0000006');