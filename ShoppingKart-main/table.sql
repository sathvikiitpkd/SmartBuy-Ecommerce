-- Entity
CREATE TABLE Users
(
    username VARCHAR(20) NOT NULL UNIQUE
    ,password VARCHAR(20) NOT NULL
    ,name VARCHAR(30) NOT NULL
    ,phoneNumber BIGINT
    ,PRIMARY KEY(username)
    ,CHECK(CHAR_LENGTH(password)>=8)
    ,CHECK(CHAR_LENGTH(username)>=4)
    ,CHECK(floor(log(abs(phoneNumber))+1) BETWEEN 9 AND 10)
);

CREATE TABLE Buyer
(
    username VARCHAR(20) NOT NULL
    ,PRIMARY KEY(username)
    ,FOREIGN KEY(username) REFERENCES Users(username)
);

CREATE TABLE Seller
(
    username VARCHAR(20) NOT NULL
    ,PRIMARY KEY(username)
    ,FOREIGN KEY(username) REFERENCES Users(username)
);

CREATE TABLE BankCard
(
    holderName VARCHAR(50) NOT NULL
    ,cardNumber BIGINT NOT NULL
    ,expiryDate DATE NOT NULL
    ,bank VARCHAR(20) NOT NULL
    ,PRIMARY KEY(cardNumber)
    ,CHECK(floor(log(abs(cardNumber))+1) BETWEEN 11 AND 12)
);

CREATE TABLE User_card
(
    username VARCHAR(20) NOT NULL
    ,cardNumber BIGINT NOT NULL
    ,PRIMARY KEY(username, cardNumber)
    ,FOREIGN KEY(username) REFERENCES Buyer(username)
    ,FOREIGN KEY(cardNumber) REFERENCES BankCard(cardNumber)
);

CREATE TABLE Address
(
    addrid SERIAL
    ,name VARCHAR(50) NOT NULL
    ,contactPhoneNumber BIGINT
    ,province VARCHAR(100)
    ,city VARCHAR(100)
    ,streetaddr VARCHAR(100) NOT NULL
    ,postCode INT NOT NULL
    ,PRIMARY KEY(addrid)
    ,CHECK(floor(log(abs(contactPhoneNumber))+1) BETWEEN 9 AND 10)
    ,CHECK(floor(log(abs(postCode))+1) BETWEEN 5 AND 6)
);

CREATE TYPE addr_category AS ENUM('home','work','friend','other', 'NONE');

CREATE TABLE User_address
(
    username VARCHAR(20) NOT NULL
    ,addrid INT NOT NULL
    ,category addr_category NOT NULL
    ,PRIMARY KEY(username, addrid)
    ,FOREIGN KEY(username) REFERENCES Buyer(username)
    ,FOREIGN KEY(addrid) REFERENCES Address(addrid)
);

CREATE TABLE Store
(
    sid SERIAL
    ,name VARCHAR(20) NOT NULL
    ,province VARCHAR(20)
    ,city VARCHAR(20)
    ,streetaddr VARCHAR(20)
    ,username VARCHAR(20) NOT NULL UNIQUE
    ,SetUpTime DATE NOT NULL DEFAULT CURRENT_DATE
    ,PRIMARY KEY(sid)
    ,FOREIGN KEY(username) REFERENCES Seller(username)
);

CREATE TABLE Product
(
    pid SERIAL
    ,name VARCHAR(100) NOT NULL
    ,type VARCHAR(50)
    ,modelNumber VARCHAR(50) UNIQUE NOT NULL
    ,color VARCHAR(50)
    ,price INT NOT NULL
    ,brandName VARCHAR(20)
    ,productGrade FLOAT
    ,PRIMARY KEY(pid)
    ,CHECK(productGrade<=5)
);

CREATE TABLE presentin
(
    pid INT NOT NULL
    ,sid INT NOT NULL
    ,quantity INT NOT NULL
    ,PRIMARY KEY(pid,sid)
    ,FOREIGN KEY(sid) REFERENCES Store(sid)
    ,FOREIGN KEY(pid) REFERENCES Product(pid)
);

CREATE TYPE status AS ENUM('success','failed');

CREATE TABLE Orders
(
    orderNumber SERIAL
    ,state status NOT NULL
    ,username VARCHAR(20) NOT NULL
    ,orderTime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    ,PRIMARY KEY (orderNumber)
    ,FOREIGN KEY(username) REFERENCES Buyer(username)
);

CREATE TABLE Comments  -- Weak Entity
(
    creationTime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    ,username VARCHAR(20) NOT NULL
    ,pid INT NOT NULL
    ,grade INT NOT NULL
    ,content VARCHAR(500)
    ,PRIMARY KEY(username,pid)
    ,FOREIGN KEY(username) REFERENCES Buyer(username)
    ,FOREIGN KEY(pid) REFERENCES Product(pid)
    ,CHECK(grade<=5)
);

CREATE TABLE Save_to_Shopping_Cart
(
    username VARCHAR(20) NOT NULL
    ,pid INT NOT NULL
    ,addTime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    ,quantity INT NOT NULL
    ,amount INT NOT NULL
    ,PRIMARY KEY (username,pid)
    ,FOREIGN KEY(username) REFERENCES Buyer(username)
    ,FOREIGN KEY(pid) REFERENCES Product(pid)
);

CREATE TABLE Payment
(
    orderNumber INT NOT NULL
    ,cardNumber BIGINT NOT NULL
    ,totalAmount INT NOT NULL
    ,PRIMARY KEY(orderNumber)
    ,FOREIGN KEY(orderNumber) REFERENCES Orders(orderNumber)
    ,FOREIGN KEY(cardNumber) REFERENCES BankCard(cardNumber)
);

CREATE TABLE Deliver_To
(
    addrid INT NOT NULL
    ,orderNumber INT NOT NULL
    ,PRIMARY KEY(orderNumber)
    ,FOREIGN KEY(addrid) REFERENCES Address(addrid)
    ,FOREIGN KEY(orderNumber) REFERENCES Orders(orderNumber)
);

CREATE TABLE Prev_orders
(
    orderNumber INT NOT NULL
    ,pid INT NOT NULL
    ,quantity INT NOT NULL
    ,amount INT NOT NULL
    ,PRIMARY KEY (pid,orderNumber)
    ,FOREIGN KEY(pid) REFERENCES Product(pid)
    ,FOREIGN KEY(orderNumber) REFERENCES Orders(orderNumber)
);
