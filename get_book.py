from ConfigParser import ConfigParser
import argparse
from DBUtils.PersistentDB import PersistentDB
import MySQLdb

_ID_TABLE = {0: "title", 1: "category", 2: "price"}

def get_data_book(username):
    password = raw_input("Password = ")
    auth = get_auth(username, password)
    if auth:
        print "SUCCESS"
        data_all = select_data()
        if data_all:
            print "|ID  |TITLE  |CATEGORY   |PRICE  "
            for data in data_all:
                print "|{0}  |{1}   |{2}   |{3} ".format(data['id'], data['title'], data['category'], data['price'])
    else:
        print "LOGIN FAILED"

def insert_data(title, category, price):
    config = "config.conf"
    conf = ConfigParser()
    conf.read(config)
    pool = PersistentDB(MySQLdb,
                        host=conf.get('database', 'dbhost'),
                        user=conf.get('database', 'dbuser'),
                        passwd=conf.get('database', 'dbpwd'),
                        db=conf.get('database', 'dbname'), charset='utf8')
    try:
        conn = pool.connection()
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        sql = "INSERT INTO book (title, category, price) VALUES ('{0}', '{1}', {2})".format(title, category, int(price))
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception:
        raise

def select_data():
    config = "config.conf"
    conf = ConfigParser()
    conf.read(config)
    pool = PersistentDB(MySQLdb,
                        host=conf.get('database', 'dbhost'),
                        user=conf.get('database', 'dbuser'),
                        passwd=conf.get('database', 'dbpwd'),
                        db=conf.get('database', 'dbname'), charset='utf8')
    conn = pool.connection()
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    sql = """SELECT * FROM book"""
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.commit()
    cursor.close()
    return  result

def add_new_data_book(username):
    password = raw_input("Password = ")
    auth = get_auth(username, password)
    if auth:
        print "SUCCESS"
        book_title = raw_input("Masukan Judul Buku = ")
        book_cat = raw_input("Masukan Kategori Buku = ")
        book_price = raw_input("Masukan Harga Buku = ")
        try:
            insert_data(book_title, book_cat, book_price)
            data_all = select_data()
            if data_all:
                print "|ID  |TITLE  |CATEGORY   |PRICE  "
                for data in data_all:
                    print "|{0}  |{1}   |{2}   |{3} ".format(data['id'], data['title'], data['category'], data['price'])
            print "FINISH"
        except Exception, e:
            print e
    else:
        print "LOGIN FAILED"

def get_auth(uname, pswd):
    config = "config.conf"
    conf = ConfigParser()
    conf.read(config)
    pool = PersistentDB(MySQLdb,
                        host=conf.get('database', 'dbhost'),
                        user=conf.get('database', 'dbuser'),
                        passwd=conf.get('database', 'dbpwd'),
                        db=conf.get('database', 'dbname'), charset='utf8')
    conn = pool.connection()
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    sql = """SELECT password FROM user WHERE username='{}'""".format(uname, pswd)
    cursor.execute(sql)
    result = cursor.fetchone()
    conn.commit()
    cursor.close()
    if result['password'] == pswd:
        return True
    else:
        return False

def update_data_book_to_db(id, col, data):
    config = "config.conf"
    conf = ConfigParser()
    conf.read(config)
    pool = PersistentDB(MySQLdb,
                        host=conf.get('database', 'dbhost'),
                        user=conf.get('database', 'dbuser'),
                        passwd=conf.get('database', 'dbpwd'),
                        db=conf.get('database', 'dbname'), charset='utf8')
    try:
        conn = pool.connection()
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        if col == 'price':
            sql = "UPDATE book SET {1} = {2} WHERE id = {0}".format(id, col, int(data))
        else:
            sql = "UPDATE book SET {1} = '{2}' WHERE id = {0}".format(id, col, data)
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception:
        raise


def update_data_book(username):
    password = raw_input("Password = ")
    auth = get_auth(username, password)
    if auth:
        print "SUCCESS"
        data_all = select_data()
        if data_all:
            print "|ID  |TITLE  |CATEGORY   |PRICE  "
            for data in data_all:
                print "|{0}  |{1}   |{2}   |{3} ".format(data['id'], data['title'], data['category'], data['price'])
            id_change = raw_input("Pilih Id Yang Akan Dirubah = ")
            id_col = raw_input("Pilih Id Coloumn Yang Akan Dirubah [TITLE[0]CATEGORY[1]PRICE[2]] = ")
            dt_change = raw_input("Masukan Data Baru = ")
            try:
                update_data_book_to_db(id_change, _ID_TABLE[int(id_col)], dt_change)
                print "UPDATE BERHASIL"
            except Exception, e:
                print e
        else:
            print "DATA TIDAK TERSEDIA"
    else:
        print "LOGIN FAILED"

def delete_data_book(username):
    password = raw_input("Password = ")
    auth = get_auth(username, password)
    if auth:
        print "SUCCESS"
        data_all = select_data()
        if data_all:
            print "|ID  |TITLE  |CATEGORY   |PRICE  "
            for data in data_all:
                print "|{0}  |{1}   |{2}   |{3} ".format(data['id'], data['title'], data['category'], data['price'])
            id_del = raw_input("Pilih Id Yang Akan Delete = ")
            try:
                delete_data_book_to_db(id_del)
                print "DELETE BERHASIL"
            except Exception, e:
                print e
        else:
            print "DATA TIDAK TERSEDIA"
    else:
        print "LOGIN FAILED"

def delete_data_book_to_db(id_delete):
    config = "config.conf"
    conf = ConfigParser()
    conf.read(config)
    pool = PersistentDB(MySQLdb,
                        host=conf.get('database', 'dbhost'),
                        user=conf.get('database', 'dbuser'),
                        passwd=conf.get('database', 'dbpwd'),
                        db=conf.get('database', 'dbname'), charset='utf8')
    try:
        conn = pool.connection()
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        sql = "DELETE FROM book WHERE id = {}".format(id_delete)
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception:
        raise

def buy_book():
    data_all = select_data()
    if data_all:
        print "|ID  |TITLE  |CATEGORY   |PRICE  "
        for data in data_all:
            print "|{0}  |{1}   |{2}   |{3} ".format(data['id'], data['title'], data['category'], data['price'])
        id_buy = raw_input("Pilih Id Yang Akan di Beli = ")
        quality = raw_input("Jumlah Yang Akan di Beli = ")
        for dt_book in data_all:
            if int(id_buy) == dt_book['id']:
                total_price = dt_book['price'] * int(quality)
                print "Total Harga Yang Harus di bayarkan = {}".format(total_price)
                try:
                    insert_data_transaction(dt_book['id'], quality, total_price)
                except Exception, e:
                    print e
                break
    else:
        print "DATA TIDAK TERSEDIA"

def insert_data_transaction(id_barang, quality, total_price):
    config = "config.conf"
    conf = ConfigParser()
    conf.read(config)
    pool = PersistentDB(MySQLdb,
                        host=conf.get('database', 'dbhost'),
                        user=conf.get('database', 'dbuser'),
                        passwd=conf.get('database', 'dbpwd'),
                        db=conf.get('database', 'dbname'), charset='utf8')
    try:
        conn = pool.connection()
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        sql = "INSERT INTO transaksi (id_barang, jumlah, total_harga) VALUES ({0}, {1}, {2})"\
                                                                            .format(id_barang, quality, total_price)
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception:
        raise

def list_data_transaction(username):
    password = raw_input("Password = ")
    auth = get_auth(username, password)
    if auth:
        print "SUCCESS"
        data_trans = select_data_transaction()
        if data_trans:
            print "|ID  |Nama Barang  |Qty   |Total harga  "
            for data in data_trans:
                print "|{0}  |{1}   |{2}   |{3} ".format(data['Id'], data['Title'], data['Qty'], data['Total_Price'])
    else:
        print "LOGIN FAILED"

def select_data_transaction():
    config = "config.conf"
    conf = ConfigParser()
    conf.read(config)
    pool = PersistentDB(MySQLdb,
                        host=conf.get('database', 'dbhost'),
                        user=conf.get('database', 'dbuser'),
                        passwd=conf.get('database', 'dbpwd'),
                        db=conf.get('database', 'dbname'), charset='utf8')
    conn = pool.connection()
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    sql = """SELECT t.id_transaksi as Id, b.title as Title, t.jumlah as Qty, t.total_harga as Total_Price 
            FROM transaksi t JOIN book b ON t.id_barang = b.id"""
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.commit()
    cursor.close()
    return  result

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='Test Aksamaraya'
                                        ,formatter_class=argparse.RawDescriptionHelpFormatter)
    argparser.add_argument('-m', '--mode', help='Mode', metavar='', default=None, type=str)
    argparser.add_argument('-u', '--username', help='Username', metavar='', default=None, type=str)
    args = argparser.parse_args()
    if args.mode == "get_list_data_book":
        get_data_book(args.username)
    elif args.mode == "add_new_data_book":
        add_new_data_book(args.username)
    elif args.mode == "update_data_book":
        update_data_book(args.username)
    elif args.mode == "delete_data_book":
        delete_data_book(args.username)
    elif args.mode == "buy_book":
        buy_book()
    elif args.mode == "list_data_transaction":
        list_data_transaction(args.username)