CREATE INDEX user_name_idx  
ON Users   
 USING HASH(username);

 CREATE INDEX buyer_idx
 on Buyer
 USING HASH(username);

 CREATE INDEX seller_idx
 on Seller
 USING HASH(username);

CREATE INDEX user_address_idx  
ON User_address
 USING HASH(addrid);

CREATE INDEX address_idx  
ON Address
USING HASH (addrid);

CREATE INDEX user_card_idx  
ON User_card
 USING HASH (cardNumber);

CREATE INDEX bankcard_idx  
ON BankCard
 USING HASH(cardNumber);

CREATE INDEX comments_idx  
ON Comments
 (username);

CREATE INDEX save_to_shopping_idx  
ON Save_to_Shopping_Cart
 USING HASH(username);

CREATE INDEX orders_idx  
ON Orders
 USING HASH(orderNumber);

CREATE INDEX payment_idx  
ON Payment
USING HASH (orderNumber);

CREATE INDEX deliver_to_idx
 on Deliver_To
USING HASH (addrid);

CREATE INDEX  usercard_idx  
ON User_card
USING HASH (username);

CREATE INDEX  store_idx  
ON Store
 USING HASH(username);

CREATE INDEX  product_idx  
ON Product
 USING HASH(pid);

 CREATE INDEX prev_orders_idx
 on Prev_orders
 USING HASH(pid)