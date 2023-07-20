-- List average ratings of all products
SELECT pid, name, AVG(grade) AS avg_rating, price 
FROM Product NATURAL JOIN Comments 
GROUP BY pid ORDER BY avg_rating DESC;

-- List of all order details payed from a given bankcard
SELECT * 
FROM Orders NATURAL JOIN Payment 
WHERE cardNumber = '1234-5678-9101' AND paymentState = 'success';

-- Details of top 10 users who have commented the most
SELECT userid, name, phoneNumber, COUNT(Comments.userid) AS no_of_comments
FROM Users NATURAL JOIN Comments 
GROUP BY userid ORDER BY no_of_comments DESC LIMIT 10;

-- Seller details of all Stores
SELECT Users.name as Seller_name, Users.phoneNumber AS Seller_PhoneNumber, Store.sid AS Store_id, Store.name AS Store_name 
FROM Users NATURAL Join Manage Join Store USING(sid);

-- List of user details and total amount spent so far
SELECT userid as id, name, SUM(totalAmount) AS totalAmount 
FROM Users NATURAL JOIN Orders 
GROUP BY userid;
