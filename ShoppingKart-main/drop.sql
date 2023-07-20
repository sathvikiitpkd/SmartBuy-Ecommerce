--  INDEX DROPPING
DROP INDEX IF EXISTS user_name_idx;
DROP INDEX IF EXISTS buyer_idx;
DROP INDEX IF EXISTS seller_idx;
DROP INDEX IF EXISTS user_address_idx;
DROP INDEX IF EXISTS address_idx;
DROP INDEX IF EXISTS user_card_idx;
DROP INDEX IF EXISTS bankcard_idx;
DROP INDEX IF EXISTS comments_idx;
DROP INDEX IF EXISTS save_to_shopping_idx;
DROP INDEX IF EXISTS orders_idx;
DROP INDEX IF EXISTS payment_idx;
DROP INDEX IF EXISTS deliver_to_idx;
DROP INDEX IF EXISTS usercard_idx;
DROP INDEX IF EXISTS store_idx;
DROP INDEX IF EXISTS product_idx;
DROP INDEX IF EXISTS prev_orders_idx;

-- Dropping Triggers
DROP TRIGGER IF EXISTS user_addr_add ON User_addresses;
DROP TRIGGER IF EXISTS user_card_add ON User_bankCard;
DROP TRIGGER IF EXISTS comment_add ON Comments_product;
DROP TRIGGER IF EXISTS saving_to_cart ON Buyer_Save_to_Cart;
DROP TRIGGER IF EXISTS updating_to_cart ON Buyer_Save_to_Cart;
DROP TRIGGER IF EXISTS user_update ON User_details;
DROP TRIGGER IF EXISTS product_insert ON product_seller;
DROP TRIGGER IF EXISTS store_update ON store_seller;

-- Dropping Functions and Procedures
DROP FUNCTION IF EXISTS category_selection;
DROP FUNCTION IF EXISTS brand_selection;
DROP FUNCTION IF EXISTS update_cart;
DROP FUNCTION IF EXISTS updating_cart;
DROP FUNCTION IF EXISTS update_addr;
DROP FUNCTION IF EXISTS update_card;
DROP FUNCTION IF EXISTS update_comment;
DROP FUNCTION IF EXISTS addr_space;
DROP FUNCTION IF EXISTS transactions;
DROP FUNCTION IF EXISTS transactions2;
DROP FUNCTION IF EXISTS user_det_update;
DROP FUNCTION IF EXISTS seller_new_prod;
DROP FUNCTION IF EXISTS seller_update_store;
DROP FUNCTION IF EXISTS login_check;
-- DROP PROCEDURE IF EXISTS delete_store;
-- DROP PROCEDURE IF EXISTS save_product_to_cart;

-- Dropping Views
-- DROP VIEW IF EXISTS product_sales_for_2022;
DROP VIEW IF EXISTS User_details;
-- DROP VIEW IF EXISTS Products_Above_Average_Price;
-- DROP VIEW IF EXISTS Buyer_Save_to_Cart;
DROP VIEW IF EXISTS User_addresses;
DROP VIEW IF EXISTS User_bankCard;
DROP VIEW IF EXISTS Comments_product;
DROP VIEW IF EXISTS Buyer_Save_to_Cart;
DROP VIEW IF EXISTS Buyer_Order_details;
DROP VIEW IF EXISTS Product_quantity;
DROP VIEW IF EXISTS product_seller;
DROP VIEW IF EXISTS store_seller;
-- DROP VIEW IF EXISTS Buyer_Order_details;
-- DROP VIEW IF EXISTS Seller_store;

-- Dropping Tables
DROP TABLE IF EXISTS Prev_orders;
DROP TABLE IF EXISTS Deliver_To;
DROP TABLE IF EXISTS Payment;
DROP TABLE IF EXISTS Save_to_Shopping_Cart;
DROP TABLE IF EXISTS Comments;
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS presentin;
DROP TABLE IF EXISTS Product;
DROP TABLE IF EXISTS Store;
DROP TABLE IF EXISTS User_address;
DROP TABLE IF EXISTS Address;
DROP TABLE IF EXISTS User_card;
DROP TABLE IF EXISTS BankCard;
DROP TABLE IF EXISTS Seller;
DROP TABLE IF EXISTS Buyer;
DROP TABLE IF EXISTS Users;
-- Dropping Datatypes
DROP TYPE IF EXISTS status;
DROP TYPE IF EXISTS addr_category;

-- Dropping Roles
DROP ROLE IF EXISTS MANAGER;
DROP ROLE IF EXISTS SELLER;
DROP ROLE IF EXISTS BUYER;
DROP ROLE IF EXISTS Likhith2;

