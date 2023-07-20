CREATE OR REPLACE VIEW User_details AS
SELECT name, phoneNumber
FROM Users
WHERE LOWER(username) = CURRENT_USER;

CREATE OR REPLACE VIEW User_addresses AS
SELECT name, contactPhoneNumber, province, city, streetaddr, postCode, category
FROM User_address NATURAL JOIN Address
WHERE LOWER(username) = CURRENT_USER;

CREATE OR REPLACE VIEW User_bankCard AS
SELECT holderName, cardNumber, expiryDate, bank
FROM User_card NATURAL JOIN BankCard
WHERE LOWER(username) = CURRENT_USER;

CREATE OR REPLACE VIEW Comments_product AS
SELECT pid, grade, content
FROM Comments NATURAL JOIN Users
WHERE LOWER(username) = CURRENT_USER;

CREATE OR REPLACE VIEW Buyer_Save_to_Cart AS
SELECT pid, quantity
FROM Save_to_Shopping_Cart
WHERE LOWER(username) = CURRENT_USER;

CREATE OR REPLACE VIEW Buyer_Order_details AS
SELECT orderNumber, totalAmount, state, orderTime
FROM Orders NATURAL JOIN Payment
WHERE LOWER(username) = CURRENT_USER;

CREATE OR REPLACE VIEW Product_quantity AS
SELECT pid, MAX(quantity) AS total_quantity
FROM presentin
GROUP BY pid;


CREATE OR REPLACE VIEW product_seller AS
SELECT sid, pid, product.name AS name, type, modelNumber, color, price, brandName, quantity
FROM product NATURAL JOIN presentin
WHERE sid IN (SELECT sid FROM Store WHERE LOWER(username)=CURRENT_USER);

CREATE OR REPLACE VIEW store_seller AS
SELECT name, province, city, streetaddr, SetUpTime
FROM Store
WHERE LOWER(username)=CURRENT_USER;

-- CREATE OR REPLACE VIEW Seller_store AS
-- SELECT Users.name AS Seller_name, phoneNumber, Store.name AS Store_name, city, customerGrade, startTime  
-- FROM Users NATURAL JOIN Manage JOIN Store USING(sid) 
-- WHERE CAST(Users.userid AS char) = CURRENT_USER;

-- CREATE OR REPLACE VIEW Products_Above_Average_Price AS
-- SELECT pid, name, price
-- FROM Product
-- WHERE price > (SELECT AVG(price) FROM Product);

-- CREATE OR REPLACE VIEW Product_Sales_For_2022 AS
-- SELECT pid, name, price
-- FROM Product
-- WHERE pid IN (SELECT pid FROM OrderItem WHERE itemid IN 
--               (SELECT itemid FROM Contain WHERE orderNumber IN
--                (SELECT orderNumber FROM Orders WHERE creationTime > '2022-01-01' AND creationTime < '2022-12-31')));
