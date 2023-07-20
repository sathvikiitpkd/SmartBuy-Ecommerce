-- 1
CREATE OR REPLACE FUNCTION category_selection()
RETURNS TABLE(category VARCHAR(50))
LANGUAGE plpgsql
AS $$
BEGIN
	RETURN QUERY SELECT DISTINCT(type) FROM Product;
END;$$;

-- 2
CREATE OR REPLACE FUNCTION brand_selection(categorySelected VARCHAR(50))
RETURNS TABLE(brand VARCHAR(20))
LANGUAGE plpgsql
AS $$
BEGIN
	if categorySelected='NONE' then
	  RETURN QUERY SELECT DISTINCT(brandName) FROM Product;
	else
	  RETURN QUERY SELECT DISTINCT(brandName) FROM Product WHERE type = categorySelected;
	end if;
END;$$;

-- 3
CREATE OR REPLACE FUNCTION update_cart()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
	DECLARE
		cost INT;
		quan INT;
   BEGIN
	  SELECT price INTO cost FROM Product WHERE pid=NEW.pid;
	  if NEW.pid IN (SELECT pid FROM Buyer_Save_to_Cart) then
	  		SELECT quantity INTO quan FROM Buyer_Save_to_Cart WHERE pid=NEW.pid;
	  		update Save_to_Shopping_Cart
			   set quantity=quan+NEW.quantity
			   		 ,amount=cost*(quan+NEW.quantity)
					 ,addTime=CURRENT_TIMESTAMP
			 where pid=NEW.pid AND username = CURRENT_USER;
	  else
			insert into save_to_shopping_cart
			values (CURRENT_USER, NEW.pid, CURRENT_TIMESTAMP, NEW.quantity, cost*(NEW.quantity));
	  end if;
	  RETURN NEW;
   END;
$$;

-- 4
-- CREATE OR REPLACE FUNCTION addr_space(addr_loc addr_category, Onumber INT)
-- RETURNS void
-- LANGUAGE plpgsql
-- AS $$
-- BEGIN
-- 	INSERT INTO Deliver_To SELECT addrid,orderNumber
-- 	from Orders NATURAL JOIN User_address where category=addr_loc AND orderNumber=Onumber;
-- END;$$;

-- 5
CREATE OR REPLACE FUNCTION transactions(addr_loc addr_category, card BIGINT)
RETURNS INT
LANGUAGE plpgsql
AS $$
DECLARE
	bill INT;
	time TIMESTAMP;
	orderID INT;
	addressID INT;
	t_row record;
	storeID INT;
	maxquan INT;
begin
	if 0 IN (SELECT COUNT(*) FROM Orders) then
	  orderID=0;
	else
	  SELECT orderNumber INTO orderID FROM Orders ORDER BY orderNumber DESC LIMIT 1;
	end if;
	SELECT CURRENT_TIMESTAMP INTO time;
	SELECT SUM(amount) INTO bill FROM Save_to_Shopping_Cart WHERE username=CURRENT_USER;
	SELECT addrid INTO addressID FROM User_address WHERE category=addr_loc AND username=CURRENT_USER;
	if addr_loc='NONE' OR card=123456789120 then
		INSERT INTO Orders VALUES (orderID+1, 'failed', CURRENT_USER, time);
		FOR t_row IN (SELECT * FROM Save_to_Shopping_Cart WHERE username=CURRENT_USER) LOOP
			INSERT INTO Prev_orders VALUES (orderID+1, t_row.pid, t_row.quantity, t_row.amount);
    	END LOOP;
		RETURN 1;
	else
		INSERT INTO Orders VALUES (orderID+1, 'success', CURRENT_USER, time);
		FOR t_row IN (SELECT * FROM Save_to_Shopping_Cart WHERE username=CURRENT_USER) LOOP
			INSERT INTO Prev_orders VALUES (orderID+1, t_row.pid, t_row.quantity, t_row.amount);
			SELECT MAX(quantity) INTO maxquan FROM presentin WHERE pid=t_row.pid GROUP BY pid;
			SELECT sid INTO storeID FROM presentin WHERE pid=t_row.pid AND quantity=maxquan;
			UPDATE presentin SET quantity = maxquan-t_row.quantity WHERE pid=t_row.pid AND sid=storeID;
    	END LOOP;
		INSERT INTO Payment VALUES (orderID+1, card, bill);
		INSERT INTO Deliver_To VALUES (addressID, orderID+1);
		DELETE FROM Save_to_Shopping_Cart WHERE username=CURRENT_USER;
		RETURN 0;
	end if;
end;$$;

-- 6
CREATE OR REPLACE FUNCTION update_card()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
if (NEW.holderName, NEW.cardNumber, NEW.expiryDate, NEW.bank) IN (SELECT * FROM BankCard) then
    if (CURRENT_USER, NEW.cardNumber) IN (SELECT * FROM User_card) then
        RAISE NOTICE 'Card already exists';
	else
		INSERT INTO User_card VALUES (CURRENT_USER, NEW.cardNumber);
    end if;
else
    INSERT INTO BankCard VALUES (NEW.holderName, NEW.cardNumber, NEW.expiryDate, NEW.bank);
	INSERT INTO User_card VALUES (CURRENT_USER, NEW.cardNumber);
end if;
RETURN NEW;
END;
$$;

-- 7
CREATE OR REPLACE FUNCTION update_addr()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
id INT;
orderID INT;
BEGIN
if 0 IN (SELECT COUNT(*) FROM Address) then
	orderID=0;
else
	SELECT addrid INTO orderID FROM Address ORDER BY addrid DESC LIMIT 1;
end if;
if (NEW.name, NEW.contactPhoneNumber, NEW.province, NEW.city, NEW.streetaddr, NEW.postCode) IN (SELECT name, contactPhoneNumber, province, city, streetaddr, postCode FROM Address) then
    SELECT addrid INTO id FROM Address WHERE name=NEW.name AND contactPhoneNumber=NEW.contactPhoneNumber AND province=NEW.province AND city=NEW.city AND streetaddr=NEW.streetaddr AND postCode=NEW.postCode;
	if (CURRENT_USER, id) IN (SELECT username, addrid FROM User_address) then
        RAISE NOTICE 'Address already exists';
	else
		INSERT INTO User_address VALUES (CURRENT_USER, id, NEW.category);
    end if;
else
    INSERT INTO Address VALUES (orderID+1, NEW.name, NEW.contactPhoneNumber, NEW.province, NEW.city, NEW.streetaddr, NEW.postCode);
	INSERT INTO User_address VALUES (CURRENT_USER, orderID+1, NEW.category);
end if;
RETURN NEW;
END;
$$;

-- 8
CREATE OR REPLACE FUNCTION update_comment()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
avg_grade INT;
BEGIN
if NEW.pid IN (SELECT pid FROM Comments_product) then
    UPDATE Comments
	SET grade=NEW.grade, content=NEW.content
	WHERE pid=NEW.pid AND username=CURRENT_USER;
else
    INSERT INTO Comments VALUES (CURRENT_TIMESTAMP, CURRENT_USER, NEW.pid, NEW.grade, NEW.content);
end if;
SELECT AVG(grade) INTO avg_grade FROM Comments WHERE pid=NEW.pid;
UPDATE Product SET productGrade=avg_grade WHERE pid=NEW.pid;
RETURN NEW;
END;
$$;

--9
CREATE OR REPLACE FUNCTION updating_cart()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
	DECLARE
		quan INT;
   BEGIN
	  if NEW.pid IN (SELECT pid FROM Buyer_Save_to_Cart) then
	  	    SELECT price INTO quan FROM product WHERE pid=NEW.pid;
	  		update Save_to_Shopping_Cart
			   set quantity= NEW.quantity
			   		,amount=(quan)*NEW.quantity
					,addtime=CURRENT_TIMESTAMP
			 where pid=NEW.pid AND username = CURRENT_USER;
	  else
			RAISE NOTICE 'Update Failed. No such product exists in your cart to update.';
	  end if;
	  DELETE FROM Save_to_Shopping_Cart WHERE quantity=0;
	  RETURN NEW;
   END;
$$;

-- 10
CREATE OR REPLACE FUNCTION transactions2()
RETURNS INT
LANGUAGE plpgsql
AS $$
declare
t_row record;
begin
	FOR t_row IN (SELECT total_quantity, quantity FROM Buyer_Save_to_Cart NATURAL JOIN Product_quantity) LOOP
        if t_row.quantity > t_row.total_quantity then
		  RETURN 1;
		end if;
    END LOOP;
	RETURN 0;
end;$$;

-- 11
CREATE OR REPLACE FUNCTION user_det_update()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
declare
oldName VARCHAR(30);
oldNumber BIGINT;
   BEGIN
	SELECT name INTO oldName FROM User_details;
	SELECT phoneNumber INTO oldNumber FROM User_details;
	  if NEW.name!=oldName then
		UPDATE Users SET name=NEW.name WHERE username=CURRENT_USER;
	  end if;
	  if NEW.phoneNumber!=oldNumber then
		UPDATE Users SET phoneNumber=NEW.phoneNumber WHERE username=CURRENT_USER;
	  end if;
	  RETURN NEW;
   END;
$$;

-- 12
CREATE OR REPLACE FUNCTION seller_new_prod()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
declare
prodID INT;
storeID INT;
   BEGIN
   	if 0 IN (SELECT COUNT(*) FROM product) then
	 	 prodID=0;
	else
	  SELECT pid INTO prodID FROM product ORDER BY pid DESC LIMIT 1;
	end if;
	if 0 IN (SELECT COUNT(*) FROM store where username=CURRENT_USER) then
	  RAISE NOTICE 'Please enter your store details before adding your products.';
	  RETURN NEW;
	else
	  SELECT sid INTO storeID FROM  store where username=CURRENT_USER;
	end if;
	INSERT INTO product VALUES (prodID+1,NEW.name,NEW.type,NEW.modelNumber,NEW.color,NEW.price,NEW.brandName);
	INSERT INTO presentin VALUES (prodID+1,storeID,NEW.quantity);
	  RETURN NEW;
   END;
$$;

-- 13
CREATE OR REPLACE FUNCTION seller_update_store()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
storeID INT;
BEGIN
if 0 IN (SELECT COUNT(*) FROM Store) then
	INSERT INTO Store VALUES (1, NEW.name, NEW.province, NEW.city, NEW.streetaddr, CURRENT_USER, NEW.SetUpTime);
else
	SELECT sid INTO storeID FROM Store ORDER BY sid DESC LIMIT 1;
	if 0 IN (SELECT COUNT(*) FROM store_seller) then
	  INSERT INTO Store VALUES (storeID+1, NEW.name, NEW.province, NEW.city, NEW.streetaddr, CURRENT_USER, NEW.SetUpTime);
	else
	  UPDATE Store SET
	  name=NEW.name
	  ,province=NEW.province
	  ,city=NEW.city
	  ,streetaddr=NEW.streetaddr
	  ,SetUpTime=NEW.SetUpTime
	  WHERE username=CURRENT_USER;
	end if;
end if;
RETURN NEW;
END;
$$;

-- 14
CREATE OR REPLACE FUNCTION login_check(username VARCHAR(20))
RETURNS INT
LANGUAGE plpgsql
AS $$
declare
begin
	IF username IN (SELECT * FROM Buyer) THEN
		RETURN 1;
	END IF;
	IF username IN (SELECT * FROM Seller) THEN
		RETURN 2;
	END IF;
	RETURN 0;
end;$$;
