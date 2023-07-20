CREATE ROLE MANAGER;
CREATE ROLE SELLER;
CREATE ROLE BUYER;

GRANT ALL ON ALL TABLES IN SCHEMA "public" to MANAGER;

GRANT SELECT
ON Product, Buyer_Order_details, Comments, presentin, Product_quantity
to BUYER;

GRANT SELECT, INSERT, UPDATE, DELETE
ON Comments, Comments_product, User_addresses, Buyer_Save_to_Cart, User_details, User_bankCard, User_card, Save_to_Shopping_Cart, BankCard, Orders, Prev_orders, Payment, Deliver_To, User_address, Address, presentin
to BUYER;

GRANT UPDATE 
ON product 
to BUYER;
-- GRANT SELECT
-- ON Seller_store
-- to SELLER;

GRANT SELECT, INSERT, UPDATE, DELETE 
ON Comments, Store, User_addresses, User_details, User_bankCard, presentin, Comments_product, User_card, BankCard, store_seller, User_address, Address, Product, product_seller, product_quantity
to SELLER;

-- GRANT ALL ON ALL TABLES IN SCHEMA "public" to SELLER;

-- CREATE ROLE dba CREATEDB LOGIN PASSWORD 'dba';
-- CREATE ROLE n1   LOGIN PASSWORD '1';
-- CREATE ROLE n2   LOGIN PASSWORD '2';
-- CREATE ROLE n3   LOGIN PASSWORD '3';
-- CREATE ROLE n4   LOGIN PASSWORD '4';

-- GRANT ADMIN to dba;
-- GRANT BUYER to n1;
-- GRANT BUYER to n2;
-- GRANT BUYER to n3;
-- GRANT BUYER to n4;

CREATE ROLE likhith2 LOGIN PASSWORD '12345678';
GRANT SELLER TO likhith2;
