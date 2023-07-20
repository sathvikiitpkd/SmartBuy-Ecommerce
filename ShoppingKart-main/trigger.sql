CREATE TRIGGER user_addr_add
INSTEAD OF INSERT
ON User_addresses
FOR EACH ROW EXECUTE PROCEDURE update_addr();

CREATE TRIGGER user_card_add
INSTEAD OF INSERT
ON User_bankCard
FOR EACH ROW EXECUTE PROCEDURE update_card();

CREATE TRIGGER comment_add
INSTEAD OF INSERT
ON Comments_product
FOR EACH ROW EXECUTE PROCEDURE update_comment();

CREATE TRIGGER saving_to_cart
INSTEAD OF INSERT
ON Buyer_Save_to_Cart
FOR EACH ROW EXECUTE PROCEDURE update_cart();

CREATE TRIGGER updating_to_cart
INSTEAD OF UPDATE
ON Buyer_Save_to_Cart
FOR EACH ROW EXECUTE PROCEDURE updating_cart();

CREATE TRIGGER user_update
INSTEAD OF UPDATE
ON User_details
FOR EACH ROW EXECUTE PROCEDURE user_det_update();

CREATE TRIGGER product_insert
INSTEAD OF INSERT
ON product_seller
FOR EACH ROW EXECUTE PROCEDURE seller_new_prod();

CREATE TRIGGER store_update
INSTEAD OF INSERT
ON store_seller
FOR EACH ROW EXECUTE PROCEDURE seller_update_store();