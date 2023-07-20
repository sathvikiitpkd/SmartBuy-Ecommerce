import streamlit as st
import sqlalchemy
from sqlalchemy.engine import create_engine
from streamlit_option_menu import option_menu
from sqlalchemy.sql import text
import pandas as pd


class PostgresqlDB:
    def __init__(self,user_name,password,host,port,db_name):
        self.user_name = user_name
        self.password = password
        self.host = host
        self.port = port
        self.db_name = db_name
        self.engine = self.create_db_engine()

    def create_db_engine(self):
        try:
            db_uri = f"postgresql+psycopg2://{self.user_name}:{self.password}@{self.host}:{self.port}/{self.db_name}"
            return create_engine(db_uri)
        except Exception as err:
            return
    def execute_dql_commands(self,stmnt,values=None):
        try:
            with self.engine.connect() as conn:
                if values is not None:
                    result = conn.execute(text(stmnt),values)
                else:
                    result = conn.execute(text(stmnt))
            return result
        except Exception as err:
            print(f'Failed to execute dql commands -- {err}')
    
    def execute_ddl_and_dml_commands(self,stmnt,values=None):
        connection = self.engine.connect()
        trans = connection.begin()
        try:
            if values is not None:

                result = connection.execute(text(stmnt),values)
            else:
                result = connection.execute(text(stmnt))
            trans.commit()
            connection.close()
            print('Command executed successfully.')
        except Exception as err:
            trans.rollback()
            print(f'Failed to execute ddl and dml commands -- {err}')
            
            
            
gname = ''
if 'active_page' not in st.session_state:
    st.session_state.active_page = 'login_or_register'
    st.session_state.check_login = 0
    st.session_state.check_register = 0
    st.session_state.l_name = ''
    st.session_state.l_pwd = ''
    st.session_state.type = ''
if 'type' not in st.session_state:
    st.session_state.type = ''

st.session_state.update(st.session_state)

def cb_login_home():
    st.session_state.active_page = 'login_home'
def cb_seller_home():
    st.session_state.active_page = 'seller_home'
def cb_sellerproduct_page(pid, sid):
    st.session_state.sellerpidvalue = pid
    st.session_state.sellerid = sid
    st.session_state.active_page = 'SellerProduct_info'
def cb_editcomment():
    st.session_state.active_page = 'edit_comment'
def cb_register_home():
    st.session_state.active_page = 'register_home'
def cb_product_page(pid):
    st.session_state.pidvalue = pid
    st.session_state.active_page = 'Product_info'
def cb_edit_address():
    st.session_state.active_page = 'Edit_Address'
def cb_edit_bank():
    st.session_state.active_page = 'Edit_Bank'
def cb_order_page(oid, statuss):
    st.session_state.orderid = oid
    st.session_state.state = statuss
    st.session_state.active_page = 'order_info'
def cb_storedetails():
    st.session_state.active_page = 'edit_store'
def cb_cust_or_emp():
    st.session_state.active_page = 'login_or_register'
def cb_login_login():
    st.session_state.check_login=1
    st.session_state.check_register=0
    st.session_state.active_page = 'authentication'
def cb_register_login():
    st.session_state.check_login=0
    st.session_state.check_register=1
    st.session_state.active_page = 'authentication'
def cb_authentication():
    st.session_state.active_page = 'authentication'

def cb_otherdetails():
    st.session_state.active_page = 'otherdetails'
 
def login(name, password):
        USER_NAME = 'postgres'
        PASSWORD = '123'
        PORT = 5432
        DATABASE_NAME = 'smartbuy'
        HOST = 'localhost'

        db = PostgresqlDB(user_name=USER_NAME,
                    password=PASSWORD,
                    host=HOST,port=PORT,
                    db_name=DATABASE_NAME)
        engine = db.engine
        username = name
        values = {'username': username,'password': password}
        select_query_stmnt = "SELECT * FROM users"
        result_1 = db.execute_dql_commands(select_query_stmnt)
        for r in result_1:
            if r.username == username and r.password == password :
                values = {'name' : username}
                select_query_stmnt123 = "SELECT login_check(:name)"
                result_123 = db.execute_dql_commands(select_query_stmnt123,values)
                for r in result_123:
                    if r[0] == 1:
                        st.session_state.type = 'Buyer'
                        return True
                    if r[0] == 2:
                        st.session_state.type = 'Seller'
                        return True
        return False

def register_insert(Name, phnumber, userName, userpassword, option) :
    USER_NAME = 'postgres'
    PASSWORD = 123
    PORT = 5432
    DATABASE_NAME = 'smartbuy'
    HOST = 'localhost'
    db = PostgresqlDB(user_name=USER_NAME,
                    password=PASSWORD,
                    host=HOST,port=PORT,
                    db_name=DATABASE_NAME)
    engine = db.engine
    Values = {'username': userName, 'password': userpassword, 'name': Name, 'phoneNumber' : phnumber}
    single_insert_stmnt = "INSERT INTO users VALUES ( :username , :password , :name , :phoneNumber );"
    db.execute_ddl_and_dml_commands(single_insert_stmnt,Values)
    if(option == 'Buyer'):
                Values = {'username': userName}
                single_insert_stmnt = "INSERT INTO Buyer VALUES ( :username );"
                db.execute_ddl_and_dml_commands(single_insert_stmnt,Values)
    if(option == 'Seller'):
                Values = {'username': userName}
                single_insert_stmnt = "INSERT INTO Seller VALUES ( :username );"
                db.execute_ddl_and_dml_commands(single_insert_stmnt,Values)
    import psycopg2
    conn = psycopg2.connect(dbname=DATABASE_NAME, user=USER_NAME, password=PASSWORD, host=HOST)
    values = {'uname': userName, 'upassword': userpassword}
    select_query_stmnt = "CREATE USER {uname} WITH PASSWORD '{upassword}'"
    with conn.cursor() as cur:
         cur.execute(select_query_stmnt.format(**values))
    values = {'option' : option, 'uname' : userName}
    select_query_stmnt = "GRANT {option} to {uname}"
    with conn.cursor() as cur:
         cur.execute(select_query_stmnt.format(**values))
         conn.commit()
    conn.close()

 
def register(Name, userName, userpassword, phnumber, option):
            register_insert(Name, phnumber, userName, userpassword, option)
            return True         

def LoggedIn_Clicked(userName, password):
        if login(userName, password):
            st.session_state.l_name = userName
            st.session_state.l_pwd = password
            if st.session_state.type == 'Buyer' :
                st.write("BUYER HOME")
                st.session_state.active_page = 'login_home'
            if st.session_state.type == 'Seller' :
                st.write("SELLER HOME")
                cb_seller_home()
        else:
            st.error("Invalid user name or password")

def registerIn_Clicked(name, userName, userpassword, phnumber, option):
        if register(name, userName, userpassword, phnumber, option):
            st.session_state.active_page = 'register_home'
        else:
            st.error("Username already exists")
            
def LoggedOut_Clicked():
         st.session_state.active_page = 'login_or_register'
                     
def authentication():
    if(st.session_state.check_login):
        st.title("Smart Buy")
        st.subheader("SignIn Portal")
        userName = st.text_input (label = "",placeholder="Enter your user name")
        password = st.text_input (label = "",placeholder="Enter password", type="password")
        st.button ("Login", on_click=LoggedIn_Clicked, args= (userName, password))
    if(st.session_state.check_register):
        st.title("Smart Buy")
        st.subheader("Registration Form")
        count = 1
        cnt = 1
        name = st.text_input("Name", key =f'{count}_{cnt}')
        cnt = 2
        userName = st.text_input("Username", key =f'{count}_{cnt}')
        cnt = 3
        userpassword = st.text_input("Password",type="password", key =f'{count}_{cnt}')
        cnt = 4
        phnumber = st.text_input("Phone Number", key =f'{count}_{cnt}')
        cnt = 5
        option = st.selectbox('Type of User',('Buyer', 'Seller'), key =f'{count}_{cnt}')
        st.button("Register", on_click=registerIn_Clicked, args= (name, userName, userpassword, phnumber, option))
        
def savingcart(pid, quantity):
    USER_NAME = st.session_state.l_name
    PASSWORD = st.session_state.l_pwd
    PORT = 5432
    DATABASE_NAME = 'smartbuy'
    HOST = 'localhost'
    db = PostgresqlDB(user_name=USER_NAME,
                    password=PASSWORD,
                    host=HOST,port=PORT,
                    db_name=DATABASE_NAME)
    engine = db.engine
    values = {'pid': pid, 'quantity': quantity}
    select_query_stmnt = "INSERT INTO Buyer_Save_to_Cart values(:pid, :quantity);"
    db.execute_ddl_and_dml_commands(select_query_stmnt,values)
    cb_login_home()

def prod_info() :
    st.sidebar.button("Back to Home Page", on_click = cb_login_home)
    st.sidebar.button("Log out", on_click= LoggedOut_Clicked)
    USER_NAME = 'postgres'
    PASSWORD = 123
    PORT = 5432
    DATABASE_NAME = 'smartbuy'
    HOST = 'localhost'
    db = PostgresqlDB(user_name=USER_NAME,
                    password=PASSWORD,
                    host=HOST,port=PORT,
                    db_name=DATABASE_NAME)
    engine = db.engine
    value = {'pid' : st.session_state.pidvalue}
    select_query_stmnt = "SELECT * FROM product where pid = :pid" 
    result_1 = db.execute_dql_commands(select_query_stmnt, value)
    st.title("Smart Buy")
    st.subheader("Product Details")
    for r in result_1:
        c1, c2 = st.columns(2)
        with c1 :
            st.write(f"Name : {r.name}")
            st.write(f"Category : {r.type}")
            st.write(f"Color : {r.color}")
            st.write(f"Brand : {r.brandname}")
            st.write(f"Model Number : {r.modelnumber}")
        with c2 :
            st.write(f"price : {r.price}")
            st.write(f"Grade : {r.productgrade}")
        st.subheader("Comments")
        value = {'pid' : st.session_state.pidvalue}
        select_query_stmnt2 = "SELECT * FROM Comments where pid = :pid" 
        result_2 = db.execute_dql_commands(select_query_stmnt2, value)
        for r2 in result_2:
            c1, c2 = st.columns(2)
            with c1 :
                st.write(f"User : {r2.username}")
                st.write(f"Comment : {r2.content}")
            with c2 :
                st.write(f"Rating : {r2.grade}")
                st.write(f"{r2.creationtime}")
            st.write("----------------------------------------")      
        st.button("Add/Edit your comment", on_click= cb_editcomment)
        st.subheader("Add to Cart")
        num = st.number_input('Enter the quantity', min_value= 1, step = 1)
        st.button("Save to Cart", on_click = savingcart, args = (r.pid, num))
        
def display_products(category, brand, name):
    USER_NAME = 'postgres'
    PASSWORD = 123
    PORT = 5432
    DATABASE_NAME = 'smartbuy'
    HOST = 'localhost'
    db = PostgresqlDB(user_name=USER_NAME,
                    password=PASSWORD,
                    host=HOST,port=PORT,
                    db_name=DATABASE_NAME)
    engine = db.engine
    select_query_stmnt = "SELECT * FROM product" 
    result_1 = db.execute_dql_commands(select_query_stmnt)
    st.subheader("Products")
    i = 0
    if brand == 'Search by Brand':
       brand = ''
    if category == 'Search by Category':
       category = ''
    for r in result_1 :
        x = "View Product " + str(i)
        i = i + 1
        if category == '' and brand == '' and name == '' :
           st.write("----------------------")
           st.write(f"Name  : {r.name}")
           st.write(f"Brand : {r.brandname}")
           st.write(f"Grade : {r.productgrade}")
           pid = r.pid
           st.button(x, on_click = cb_product_page, args=[pid])
        if category == r.type and brand == r.brandname and name == r.name :
           st.write("----------------------")
           st.write(f"Name  : {r.name}")
           st.write(f"Brand : {r.brandname}")
           st.write(f"Grade : {r.productgrade}")
           pid = r.pid
           st.button(x, on_click = cb_product_page,args=[pid])
        if category == '' and brand == r.brandname and name == r.name :
           st.write("----------------------")
           st.write(f"Name  : {r.name}")
           st.write(f"Brand : {r.brandname}")
           st.write(f"Grade : {r.productgrade}")
           pid = r.pid
           st.button(x, on_click = cb_product_page, args=[pid])
        if category == r.type and brand == '' and name == r.name :
           st.write("----------------------")
           st.write(f"Name  : {r.name}")
           st.write(f"Brand : {r.brandname}")
           st.write(f"Grade : {r.productgrade}")
           pid = r.pid
           st.button(x, on_click = cb_product_page, args=[pid])
        if category == r.type and brand == r.brandname and name == '' :
           st.write("----------------------")
           st.write(f"Name  : {r.name}")
           st.write(f"Brand : {r.brandname}")
           st.write(f"Grade : {r.productgrade}")
           pid = r.pid
           st.button(x, on_click = cb_product_page, args=[pid])
        if category == '' and brand == '' and name == r.name :
           st.write("----------------------")
           st.write(f"Name  : {r.name}")
           st.write(f"Brand : {r.brandname}")
           st.write(f"Grade : {r.productgrade}")
           pid = r.pid
           st.button(x, on_click = cb_product_page, args=[pid])
        if category == r.type and brand == '' and name == '' :
           st.write("----------------------")
           st.write(f"Name  : {r.name}")
           st.write(f"Brand : {r.brandname}")
           st.write(f"Grade : {r.productgrade}")
           pid = r.pid
           st.button(x, on_click = cb_product_page,args = [pid])
        if category == '' and brand == r.brandname and name == '' :
           st.write("----------------------")
           st.write(f"Name  : {r.name}")
           st.write(f"Brand : {r.brandname}")
           st.write(f"Grade : {r.productgrade}")
           pid = r.pid
           st.button(x, on_click = cb_product_page, args=[pid])
         
def not_yet_clicked():
    USER_NAME = 'postgres'
    PASSWORD = 123
    PORT = 5432
    DATABASE_NAME = 'smartbuy'
    HOST = 'localhost'
    db = PostgresqlDB(user_name=USER_NAME,
                    password=PASSWORD,
                    host=HOST,port=PORT,
                    db_name=DATABASE_NAME)
    engine = db.engine
    select_query_stmnt = "SELECT * FROM product LIMIT 10" 
    st.subheader("Products")
    result_1 = db.execute_dql_commands(select_query_stmnt)
    for r in result_1 :
           st.write("----------------------")
           st.write(f"Name  : {r.name}")
           st.write(f"Brand : {r.brandname}")
           st.write(f"Grade : {r.productgrade}")
           pid = r.pid
           x = "View Product " + str(pid)
           st.button(x, on_click = cb_product_page, args=[pid])
        
def unique_category_list():
    USER_NAME = 'postgres'
    PASSWORD = 123
    PORT = 5432
    DATABASE_NAME = 'smartbuy'
    HOST = 'localhost'
    db = PostgresqlDB(user_name=USER_NAME,
                    password=PASSWORD,
                    host=HOST,port=PORT,
                    db_name=DATABASE_NAME)
    engine = db.engine
    select_query_stmnt = "SELECT * FROM category_selection()" 
    result_1 = db.execute_dql_commands(select_query_stmnt)
    l = []
    l.append('Search by Category')
    for r in result_1 :
        l.append(r.category)
    return l
    
def unique_brand_list(option1):
    if option1 == 'Search by Category':
       option1 = 'NONE'
    USER_NAME = 'postgres'
    PASSWORD = 123
    PORT = 5432
    DATABASE_NAME = 'smartbuy'
    HOST = 'localhost'
    db = PostgresqlDB(user_name=USER_NAME,
                    password=PASSWORD,
                    host=HOST,port=PORT,
                    db_name=DATABASE_NAME)
    engine = db.engine
    value = {'category': option1}
    select_query_stmnt = "SELECT * FROM brand_selection(:category)" 
    result_1 = db.execute_dql_commands(select_query_stmnt, value)
    l = []
    l.append('Search by Brand')
    for r in result_1 :
        l.append(r.brand)
    return l

def update_cart_fun(pid, quantity):
    USER_NAME = st.session_state.l_name
    PASSWORD = st.session_state.l_pwd
    PORT = 5432
    DATABASE_NAME = 'smartbuy'
    HOST = 'localhost'
    db = PostgresqlDB(user_name=USER_NAME,
                    password=PASSWORD,
                    host=HOST,port=PORT,
                    db_name=DATABASE_NAME)
    engine = db.engine
    values = {'pid': pid, 'quantity': quantity}
    select_query_stmnt = "UPDATE Buyer_Save_to_Cart values SET quantity = :quantity WHERE pid = :pid;"
    db.execute_ddl_and_dml_commands(select_query_stmnt,values)
    cb_login_home()
    
def order_now():
    USER_NAME = st.session_state.l_name
    PASSWORD = st.session_state.l_pwd
    PORT = 5432
    DATABASE_NAME = 'smartbuy'
    HOST = 'localhost'
    db = PostgresqlDB(user_name=USER_NAME,
                    password=PASSWORD,
                    host=HOST,port=PORT,
                    db_name=DATABASE_NAME)
    select_query_stmnt10 = "SELECT transactions2()"
    result10 = db.execute_dql_commands(select_query_stmnt10)
    for r2 in result10:
        if r2.transactions2 == 1 :
            st.error("Quantity ordered for one of your products exceeds supply quantity")
        else :
            st.info(f"Order processing...")
            cb_otherdetails()

def cart_products():
    USER_NAME = st.session_state.l_name
    PASSWORD = st.session_state.l_pwd
    PORT = 5432
    DATABASE_NAME = 'smartbuy'
    HOST = 'localhost'
    db = PostgresqlDB(user_name=USER_NAME,
                    password=PASSWORD,
                    host=HOST,port=PORT,
                    db_name=DATABASE_NAME)
    engine = db.engine
    select_query_stmnt = "SELECT * FROM save_to_shopping_cart ORDER BY pid;" 
    result = db.execute_dql_commands(select_query_stmnt) 
    total_amount = 0
    for r in result:
        select_query_stmnt1 = "SELECT name FROM product where pid = :pid ORDER BY pid;"
        values = {'pid' : r.pid}
        result1 = db.execute_dql_commands(select_query_stmnt1, values) 
        st.write("----------------------")
        st.write(f"Product Id : {r.pid}")
        for r1 in result1:
            st.write(f"Product Name  : {r1.name}")
        st.write(f"Addtime : {r.addtime}")
        x = 'Quantity of pid ' + str(r.pid)
        num = st.number_input(x, value = r.quantity, step = 1, min_value = 0)
        update_cart_fun(r.pid, num)
        st.write(f"Amount : {r.amount}")
        total_amount = total_amount + r.amount
        x = "View Product " + str(r.pid)
        st.button(x, on_click = cb_product_page, args =[r.pid])
    st.subheader(f"Total Amount : {total_amount}")
    st.button("Order Now", on_click = order_now)

def proceedfun(option1, option2) :
    USER_NAME = st.session_state.l_name
    PASSWORD = st.session_state.l_pwd
    PORT = 5432
    DATABASE_NAME = 'smartbuy'
    HOST = 'localhost'
    import psycopg2
    conn = psycopg2.connect(dbname=DATABASE_NAME, user=USER_NAME, password=PASSWORD, host=HOST)
    if option1 == 'Select Address':
            option1 = 'NONE'
    if option2 == 'Select BankCard':
            option2 = 123456789120
    values = {'option1' : option1, 'option2' : option2}
    select_query_stmnt = "SELECT * from transactions('{option1}', {option2})"
    with conn.cursor() as cur:
        cur.execute(select_query_stmnt.format(**values))
        result_1 = cur.fetchall()
        for r2 in result_1:
            if r2[0] == 0 :
                st.info("Transaction Success")
            else :
                st.error("Transaction Failure")
        conn.commit()
    cb_login_home()

def otherdetails():
    USER_NAME = st.session_state.l_name
    PASSWORD = st.session_state.l_pwd
    PORT = 5432
    DATABASE_NAME = 'smartbuy'
    HOST = 'localhost'
    db = PostgresqlDB(user_name=USER_NAME,
                    password=PASSWORD,
                    host=HOST,port=PORT,
                    db_name=DATABASE_NAME)
    engine = db.engine
    st.sidebar.button("Back to Home Page", on_click = cb_login_home)
    st.sidebar.button("Log out", on_click= LoggedOut_Clicked)
    st.header("Ordering ...")
    st.subheader("Select Address")
    select_query_stmnt = "SELECT category FROM user_addresses" 
    result_1 = db.execute_dql_commands(select_query_stmnt)
    l = []
    l.append('Select Address')
    for r in result_1 :
        l.append(r.category)
    option1 = st.selectbox('', l)
    st.subheader("Select BankCard")
    select_query_stmnt = "SELECT cardnumber FROM user_bankcard" 
    result_1 = db.execute_dql_commands(select_query_stmnt)
    l = []
    l.append('Select BankCard')
    for r in result_1 :
        l.append(r.cardnumber)
    option2 = st.selectbox('', l)
    click = st.button("Proceed", on_click = proceedfun, args = (option1, option2))
    
def change_name(phonenumber):
    USER_NAME = st.session_state.l_name
    PASSWORD = st.session_state.l_pwd
    PORT = 5432
    DATABASE_NAME = 'smartbuy'
    HOST = 'localhost'
    db = PostgresqlDB(user_name=USER_NAME,
                    password=PASSWORD,
                    host=HOST,port=PORT,
                    db_name=DATABASE_NAME)
    engine = db.engine
    values = {'name' : st.text_input("", placeholder= "Enter your Full Name"), 'phoneNumber' : phonenumber}
    select_query_stmnt5 = "INSERT INTO User_details values(:name, :phoneNumber)" 
    db.execute_dql_commands(select_query_stmnt5, values)

def display_personal_details():
    USER_NAME = st.session_state.l_name
    PASSWORD = st.session_state.l_pwd
    PORT = 5432
    DATABASE_NAME = 'smartbuy'
    HOST = 'localhost'
    db = PostgresqlDB(user_name=USER_NAME,
                    password=PASSWORD,
                    host=HOST,port=PORT,
                    db_name=DATABASE_NAME)
    engine = db.engine
    select_query_stmnt = "SELECT * FROM User_details" 
    result = db.execute_dql_commands(select_query_stmnt)
    for r in result : 
        st.write(f"Full Name      :                    {r.name}")
        st.write(f"Phone Number   :                 {r.phonenumber}")
        st.write("-----------------------------------------------------------")
    select_query_stmnt = "SELECT * FROM user_addresses" 
    result = db.execute_dql_commands(select_query_stmnt)
    st.subheader("Address Details")
    for r in result : 
        st.write(f"Name      :                    {r.name}")
        st.write(f"ContactPhoneNumber   :                 {r.contactphonenumber}")
        st.write(f"Street Address      :                    {r.streetaddr}")
        st.write(f"Province    :                    {r.province}")
        st.write(f"City   :                 {r.city}")
        st.write(f"Post Code   :                 {r.postcode}")
        st.write(f"Category    :                    {r.category}")
        st.write("-----------------------------------------------------------")
    st.button("Edit Address", on_click = cb_edit_address)
    select_query_stmnt = "SELECT * FROM User_bankCard" 
    result = db.execute_dql_commands(select_query_stmnt)
    st.subheader("Bank Card Details")
    for r in result : 
        st.write(f"Card Holder Name      :                    {r.holdername}")
        st.write(f"Card Number   :                 {r.cardnumber}")
        st.write(f"Expiry Date      :                    {r.expirydate}")
        st.write(f"Bank    :                    {r.bank}")
        st.write("-----------------------------------------------------------")
    st.button("Edit Bank Details", on_click = cb_edit_bank)

def your_orders() :
    USER_NAME = st.session_state.l_name
    PASSWORD = st.session_state.l_pwd
    PORT = 5432
    DATABASE_NAME = 'smartbuy'
    HOST = 'localhost'
    db = PostgresqlDB(user_name=USER_NAME,
                    password=PASSWORD,
                    host=HOST,port=PORT,
                    db_name=DATABASE_NAME)
    engine = db.engine
    
    select_query_stmnt = "SELECT * FROM Orders ORDER BY ordertime DESC" 
    result = db.execute_dql_commands(select_query_stmnt)
    c1, c2, c3, c4 = st.columns([1,1.2,2.5,1.2])
    with c1 :
        st.write("Order Number")
    with c2 :
        st.write("Payment Status")
    with c3 :
        st.write("OrderTime")
    with c4 :
        st.write("View Orders")
    for r in result : 
        with c1 :    
            st.write(f"{r.ordernumber}")
            st.write("\n")
            st.write("-----------------\n")
        with c2 :
            st.write(r.state)
            st.write("\n")
            st.write("-----------------\n")
        with c3 :
            st.write(f"{r.ordertime}")
            st.write("\n")
            st.write("-----------------\n")
        with c4 :
            x = 'View Orders ' + str(r.ordernumber)
            st.button(x, on_click = cb_order_page, args = (r.ordernumber, r.state))
            st.write("-------------------\n")

def orderinfo():
    st.header("Order Details")
    st.sidebar.button("Back to Home Page", on_click = cb_login_home)
    st.sidebar.button("Log out", on_click= LoggedOut_Clicked)
    USER_NAME = st.session_state.l_name
    PASSWORD = st.session_state.l_pwd
    PORT = 5432
    DATABASE_NAME = 'smartbuy'
    HOST = 'localhost'
    db = PostgresqlDB(user_name=USER_NAME,
                    password=PASSWORD,
                    host=HOST,port=PORT,
                    db_name=DATABASE_NAME)
    engine = db.engine
    values = {'oid' : st.session_state.orderid} 
    select_query_stmnt = "SELECT pid, name, color, brandname, modelnumber, quantity, amount FROM prev_orders NATURAL JOIN product where orderNumber = :oid" 
    result = db.execute_dql_commands(select_query_stmnt, values)
    df = pd.DataFrame(result)
    df.index = [df.index+1]
    st.table(df)
    result1 = db.execute_dql_commands(select_query_stmnt, values)
    total_amount = 0
    for r in result1:
        total_amount += r.amount
    st.write(f"Total Amount for this order : {total_amount}")
    if st.session_state.state == 'success':
        st.subheader("Payment Details")
        select_query_stmnt = "SELECT holdername, cardnumber, bank FROM payment NATURAL JOIN bankcard where orderNumber = :oid" 
        result = db.execute_dql_commands(select_query_stmnt, values)
        for r in result:
            st.write(f"Holder Name: {r.holdername}")
            st.write(f"Card Number: {r.cardnumber}")
            st.write(f"Bank Name  : {r.bank}")
        st.subheader("Delivered to")
        select_query_stmnt1 = "SELECT name, contactphonenumber, province, city, streetaddr, postcode FROM deliver_to NATURAL JOIN address where orderNumber = :oid" 
        result1 = db.execute_dql_commands(select_query_stmnt1, values)
        for r in result1:
            st.write(f"Name              : {r.name}")
            st.write(f"ContactPhoneNumber: {r.contactphonenumber}")
            st.write(f"Province          : {r.province}")
            st.write(f"City              : {r.city}")
            st.write(f"Street Address    : {r.streetaddr}")
            st.write(f"Post Code         : {r.postcode}")

def login_home():
    with st.sidebar :
         selected = option_menu(st.session_state.l_name , ['Search', 'Profile', 'Cart', 'Orders'], icons=['search', 'person', "cart", 'list-task'], 
    menu_icon="house")
    st.sidebar.button("Log Out", on_click = LoggedOut_Clicked)
    if selected == 'Profile' :
       st.header("Smart Buy")
       st.subheader("Personal Details")
       display_personal_details() 
    if selected == 'Search' :
       st.title("Smart Buy")
       st.header("Search")
       st.subheader("Filters")
       category_list = unique_category_list()
       #st.write(category_list)
       option1 = st.selectbox('', category_list)
       brand_list = unique_brand_list(option1)
       option2 = st.selectbox('', brand_list)
       option3 = st.text_input(label = "",placeholder="Enter your product name")
       clicked = st.button("Search")
       if clicked :
          display_products(option1, option2, option3)
       else :
          not_yet_clicked()
    if selected == 'Cart' :
        st.subheader("Your Cart")
        cart_products()
    if selected == 'Orders' :
        st.subheader("Your Orders")
        your_orders()
          
def register_home():
    st.title("Smart Buy")
    st.subheader("Successful Registration")
    st.button("Go to main page", on_click = LoggedOut_Clicked)     
      
def login_or_register():
    st.title("Smart Buy")
    st.subheader("Do you want to login or register?")
    c1, c2 = st.columns(2)
    with c1:
        st.button("login", on_click=cb_login_login)
    with c2:
        st.button("register", on_click=cb_register_login)       

def editadd(name, contactPhoneNumber, province, city, streetaddr, postcode, option):
    USER_NAME = st.session_state.l_name
    PASSWORD = st.session_state.l_pwd
    DATABASE_NAME = 'smartbuy'
    HOST = 'localhost'
    
    import psycopg2
    conn = psycopg2.connect(dbname=DATABASE_NAME, user=USER_NAME, password=PASSWORD, host=HOST)
    values = {'name' : name, 'contactPhoneNumber' : contactPhoneNumber, 'province' : province, 'city' : city, 'streetaddr' : streetaddr, 'postcode' : postcode, 'category' : option}
    select_query_stmnt = "INSERT INTO user_addresses values('{name}' , {contactPhoneNumber}, '{province}', '{city}', '{streetaddr}', {postcode}, '{category}')"
    with conn.cursor() as cur:
         cur.execute(select_query_stmnt.format(**values))
         conn.commit()
    conn.close()

def editaddressclicked(name, contactPhoneNumber, province, city, streetaddr, postcode, option) :
    editadd(name, contactPhoneNumber, province, city, streetaddr, postcode, option)
    cb_login_home()

def editaddress():
    st.header("Add/Edit Address")
    st.sidebar.button("Back to Home Page", on_click = cb_login_home)
    st.sidebar.button("Log out", on_click= LoggedOut_Clicked)
    option = st.selectbox('Select Category',('home', 'work', 'friend', 'other'))
    name = st.text_input("",placeholder = "Please type the Name")
    contactPhoneNumber = st.number_input("ContactPhoneNumber", step = 10000)
    province = st.text_input("",placeholder = "Please enter the Province")
    city = st.text_input("",placeholder = "Please enter the City")
    streetaddr = st.text_input("",placeholder = "Please enter the street address")
    postcode = st.number_input("postcode", step = 10000)
    st.button("Submit", on_click = editaddressclicked, args = (name, contactPhoneNumber, province, city, streetaddr, postcode, option))

def editbankclicked(holdername, banknumber, expirydate, bank):
    USER_NAME = st.session_state.l_name
    PASSWORD = st.session_state.l_pwd
    DATABASE_NAME = 'smartbuy'
    HOST = 'localhost'
    import psycopg2
    conn = psycopg2.connect(dbname=DATABASE_NAME, user=USER_NAME, password=PASSWORD, host=HOST)
    values = {'holdername' : holdername, 'banknumber' : banknumber, 'expirydate' : expirydate, 'bank' : bank}
    select_query_stmnt = "INSERT INTO user_bankcard values('{holdername}' , {banknumber}, '{expirydate}', '{bank}')"
    with conn.cursor() as cur:
         cur.execute(select_query_stmnt.format(**values))
         conn.commit()
    conn.close()
    cb_login_home()
    
def editbank():
    st.header("Add/Edit Bank Details")
    st.sidebar.button("Back to Home Page", on_click = cb_login_home)
    st.sidebar.button("Log out", on_click= LoggedOut_Clicked)
    holdername = st.text_input("",placeholder = "Please type the Bank holder name")
    banknumber = st.number_input("BankNumber", step = 10000)
    expirydate = st.date_input("Expiry Date")
    bank = st.text_input("Bank")
    st.button("Submit", on_click = editbankclicked, args = (holdername, banknumber, expirydate, bank))

def edit_comment(rating, content):
    USER_NAME = st.session_state.l_name
    PASSWORD = st.session_state.l_pwd
    PORT = 5432
    DATABASE_NAME = 'smartbuy'
    HOST = 'localhost'
    db = PostgresqlDB(user_name=USER_NAME,
                    password=PASSWORD,
                    host=HOST,port=PORT,
                    db_name=DATABASE_NAME)
    engine = db.engine
    st.success("Added comment successfully")
    values = {'pid': st.session_state.pidvalue, 'option' : rating, 'content' : content}
    select_query_stmnt = "INSERT INTO Comments_product values(:pid, :option, :content);"
    db.execute_ddl_and_dml_commands(select_query_stmnt,values)
    cb_product_page(st.session_state.pidvalue)

def editcomment():
    st.header("Want to edit/add your comment!!")
    st.sidebar.button("Back to Home Page", on_click = cb_login_home)
    st.sidebar.button("Log out", on_click= LoggedOut_Clicked)  
    option = st.number_input('Rating', step = 1, max_value= 5, min_value= 1)
    content = st.text_input("Add your comment", placeholder = "Less than 500 characters",max_chars = 500)
    st.button("Add/Edit Comment", on_click = edit_comment, args = (option, content))

def sellerdisplaydetails():
    USER_NAME = st.session_state.l_name
    PASSWORD = st.session_state.l_pwd
    PORT = 5432
    DATABASE_NAME = 'smartbuy'
    HOST = 'localhost'
    db = PostgresqlDB(user_name=USER_NAME,
                    password=PASSWORD,
                    host=HOST,port=PORT,
                    db_name=DATABASE_NAME)
    engine = db.engine
    select_query_stmnt = "SELECT * FROM User_details" 
    result = db.execute_dql_commands(select_query_stmnt)
    for r in result : 
        st.write(f"Full Name      :                    {r.name}")
        st.write(f"Phone Number   :                 {r.phonenumber}")
        st.write("-----------------------------------------------------------")
    st.subheader("Store Details")
    select_query_stmnt1234 = "SELECT * FROM store_seller" 
    result = db.execute_dql_commands(select_query_stmnt1234)
    if result :
        for r in result :
            st.write(f"Store Name      :                    {r.name}")
            st.write(f"Street Address      :                    {r.streetaddr}")
            st.write(f"Province      :                    {r.province}")
            st.write(f"City      :                    {r.city}")
            st.write(f"Store SetUpTime      :                    {r.setuptime}")
            st.write("----------------------------------------------------------")
    st.button("Edit Store Address", on_click = cb_storedetails)

def display_sellerproducts(name):
     USER_NAME = st.session_state.l_name
     PASSWORD = st.session_state.l_pwd
     PORT = 5432
     DATABASE_NAME = 'smartbuy'
     HOST = 'localhost'
     db = PostgresqlDB(user_name=USER_NAME,
         password=PASSWORD,
         host=HOST,port=PORT,
         db_name=DATABASE_NAME)
     engine = db.engine
     values = {'name' : name}
     select_query_stmnt = "SELECT * FROM product_seller where name = :name"
     result_1 = db.execute_dql_commands(select_query_stmnt, values)
     for r in result_1:
         if r.name == name :
             st.write("----------------------")
             st.write(f"Name  : {r.name}")
             st.write(f"Brand Name : {r.brandname}")
             st.write(f"Product Category : {r.type}")
             pid = r.pid
             x = "View Product" + str(pid)
             value = {'name' : st.session_state.l_name}
             select_query_stmnt_1 = "SELECT sid FROM product_seller limit 1"
             result1 = db.execute_dql_commands(select_query_stmnt_1, value)
             for ra in result1 :
                 st.button(x, on_click = cb_sellerproduct_page, args=(pid, ra.sid))

def notsellerclicked():
    USER_NAME = st.session_state.l_name
    PASSWORD = st.session_state.l_pwd
    PORT = 5432
    DATABASE_NAME = 'smartbuy'
    HOST = 'localhost'
    db = PostgresqlDB(user_name=USER_NAME,
         password=PASSWORD,
         host=HOST,port=PORT,
         db_name=DATABASE_NAME)
    engine = db.engine
    select_query_stmnt = "SELECT * FROM product_seller"
    result_1 = db.execute_dql_commands(select_query_stmnt)
    for r in result_1:
             st.write("----------------------")
             st.write(f"Name  : {r.name}")
             st.write(f"Brand Name : {r.brandname}")
             st.write(f"Product Category : {r.type}")
             pid = r.pid
             x = "View Product" + str(pid)
             value = {'name' : st.session_state.l_name}
             select_query_stmnt_1 = "SELECT sid FROM product_seller limit 1"
             result1 = db.execute_dql_commands(select_query_stmnt_1, value)
             for ra in result1 :
                 st.button(x, on_click = cb_sellerproduct_page, args=(pid, ra.sid))

def add_product(name, type, modelnumber, color, price, brandname, quantity):
    USER_NAME = st.session_state.l_name
    PASSWORD = st.session_state.l_pwd
    PORT = 5432
    DATABASE_NAME = 'smartbuy'
    HOST = 'localhost'
    db = PostgresqlDB(user_name=USER_NAME,
         password=PASSWORD,
         host=HOST,port=PORT,
         db_name=DATABASE_NAME)
    engine = db.engine
    values = {'name' : name, 'type' : type, 'modelnumber' : modelnumber, 'color' : color, 'price' : price, 'brandname' : brandname, 'quantity' : quantity}
    select_query_stmnt12 = "select count(*) from (Select * from product where modelnumber = :modelnumber) as qwerty"
    result = db.execute_dql_commands(select_query_stmnt12,values)
    for r in result : 
        if r[0] != 0:
            st.info("Product already exists. Please check your product details")
        else :
            select_query_stmnt = "INSERT INTO product_seller(name, type, modelnumber, color, price, brandname, quantity) values(:name, :type, :modelnumber, :color, :price, :brandname, :quantity)"
            db.execute_ddl_and_dml_commands(select_query_stmnt,values)
            select_query_stmnt12 = "Select * from product where modelnumber = :modelnumber"
            result = db.execute_dql_commands(select_query_stmnt12,values)
            if result :
                st.success("Product added successfully")
            else :
                st.error("Product addition failed")

def addproduct():
    name = st.text_input("", placeholder = "Product Name")
    type = st.text_input("", placeholder = "Enter the category of product")
    modelnumber = st.text_input("", placeholder = "Type the model number")
    color = st.text_input("", placeholder = "Type the color of the product")
    price = st.number_input("Price", min_value = 0, step = 1)
    brandname = st.text_input("", placeholder = "Type the brandname of the product")
    quantity = st.number_input("Quantity", min_value = 1, step = 1)
    st.button("Add Product", on_click = add_product, args = (name, type, modelnumber, color, price, brandname, quantity))
    #product_seller
def sellerhome()  :
    with st.sidebar :
         selected = option_menu(st.session_state.l_name , ['View Products', 'Add Product', 'Profile'], icons=['products', 'products', 'person'], 
    menu_icon="house")
    st.sidebar.button("Log Out", on_click = LoggedOut_Clicked)
    if selected == 'Profile' :
        st.header("Smart Buy")
        st.subheader("Personal Details")
        sellerdisplaydetails()
    if selected == 'Add Product' :
       st.subheader("Please add your Product") 
       addproduct()
    if selected == 'View Products':
        st.header("Smart Buy")
        st.subheader("Search By Product Name")
        name = st.text_input(label = "",placeholder="Enter product name")
        check = st.button("Search")
        if check :
           display_sellerproducts(name)
        else :
            notsellerclicked()

def editstore():
    st.subheader("Store Details Please !!!")
    name = st.text_input("",placeholder = "Please type the Store name")
    streetaddr = st.text_input("",placeholder = "Please type the Street Address")
    province = st.text_input("",placeholder = "Please type the Province")
    city = st.text_input("",placeholder = "Please type the city")
    SetUpTime = st.date_input("Store Set Up Time")
    st.button("Submit", on_click= storeinsert, args= (name, province, city, streetaddr, SetUpTime))

def storeinsert(name, province, city, streetaddr, SetUpTime):
    USER_NAME = st.session_state.l_name
    PASSWORD = st.session_state.l_pwd
    PORT = 5432
    DATABASE_NAME = 'smartbuy'
    HOST = 'localhost'
    db = PostgresqlDB(user_name=USER_NAME,
                    password=PASSWORD,
                    host=HOST,port=PORT,
                    db_name=DATABASE_NAME)
    engine = db.engine
    values = {'name' : name , 'province' : province, 'city' : city, 'streetaddr' : streetaddr, 'SetUpTime' : SetUpTime}
    select_query_stmnt = "INSERT INTO  store_seller values(:name, :province, :city, :streetaddr, :SetUpTime);"
    db.execute_ddl_and_dml_commands(select_query_stmnt,values)
    st.success("Store Details added or updated successfully")
    cb_seller_home()

def sellerproduct(num):
    USER_NAME = st.session_state.l_name
    PASSWORD = st.session_state.l_pwd
    PORT = 5432
    DATABASE_NAME = 'smartbuy'
    HOST = 'localhost'
    db = PostgresqlDB(user_name=USER_NAME,
                    password=PASSWORD,
                    host=HOST,port=PORT,
                    db_name=DATABASE_NAME)
    engine = db.engine
    value = {'quantity' : num, 'pid' : st.session_state.sellerpidvalue, 'sid' : st.session_state.sellerid}
    select_query_statement = "UPDATE presentin set quantity = :quantity where pid = :pid and sid = :sid"
    db.execute_ddl_and_dml_commands(select_query_statement,value)
    st.success("Product quantity updated")
    st.subheader("Comments")
    cb_sellerproduct_page(st.session_state.sellerpidvalue, st.session_state.sellerid)


def sellerproductinfo():
    st.sidebar.button("Back to Home Page", on_click = cb_seller_home)
    st.sidebar.button("Log out", on_click= LoggedOut_Clicked)
    USER_NAME = st.session_state.l_name
    PASSWORD = st.session_state.l_pwd
    PORT = 5432
    DATABASE_NAME = 'smartbuy'
    HOST = 'localhost'
    db = PostgresqlDB(user_name=USER_NAME,
                    password=PASSWORD,
                    host=HOST,port=PORT,
                    db_name=DATABASE_NAME)
    engine = db.engine
    value = {'pid' : st.session_state.sellerpidvalue, 'sid' : st.session_state.sellerid}
    select_query_stmnt = "SELECT * FROM product_seller where pid = :pid and sid = :sid" 
    result_1 = db.execute_dql_commands(select_query_stmnt, value)
    st.title("Smart Buy")
    st.subheader("Product Details")
    for r in result_1:
        c1, c2 = st.columns(2)
        with c1 :
            st.write(f"Name : {r.name}")
            st.write(f"Category : {r.type}")
            st.write(f"Color : {r.color}")
            st.write(f"Brand : {r.brandname}")
        with c2 :
            st.write(f"Model Number : {r.modelnumber}")
            st.write(f"price : {r.price}")
        num = st.number_input('Enter the quantity', value = r.quantity, step = 1, min_value=0)
        st.button("Edit", on_click = sellerproduct, args = [num])
    st.subheader("Comments")
    value = {'pid' : st.session_state.sellerpidvalue}
    select_query_stmnt = "SELECT * FROM Comments where pid = :pid" 
    result_1 = db.execute_dql_commands(select_query_stmnt, value)
    for r in result_1:
            c1, c2 = st.columns(2)
            with c1 :
                st.write(f"User : {r.username}")
                st.write(f"Comment : {r.content}")
            with c2 :
                st.write(f"Rating : {r.grade}")
                st.write(f"{r.creationtime}")
            st.write("----------------------------------------")   
if st.session_state.active_page == 'login_home':
    login_home()

elif st.session_state.active_page == 'register_home':
    register_home()

elif st.session_state.active_page == 'authentication':
    authentication()

elif st.session_state.active_page == 'login_or_register':
    login_or_register()
    
elif st.session_state.active_page == 'Product_info':
    prod_info()

elif st.session_state.active_page == 'otherdetails':
    otherdetails()
    
elif st.session_state.active_page == 'order_info' :
    orderinfo()

elif st.session_state.active_page == 'Edit_Address' :
    editaddress()

elif st.session_state.active_page == 'Edit_Bank' :
    editbank()

elif st.session_state.active_page == 'edit_comment' :
    editcomment()

elif st.session_state.active_page == 'seller_home' :
    sellerhome()

elif st.session_state.active_page == 'edit_store':
    editstore()
elif st.session_state.active_page == 'SellerProduct_info':
    sellerproductinfo()