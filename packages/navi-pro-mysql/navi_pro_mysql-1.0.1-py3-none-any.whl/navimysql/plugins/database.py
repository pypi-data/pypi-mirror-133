#commented out sql and import
#import sqlite3
#from sqlite3 import Error

#added below two lines
import mysql.connector
from mysql.connector import Error

import click
# import time

#need to detminer what db_File does
def new_db_connection():
#def new_db_connection(db_file):
    # create a connection to our database
       
    
 
    conn = None
    
    try:
        # A database file will be created if one doesn't exist
        #commented sqlite3
        #conn = sqlite3.connect(db_file, timeout=10.0)
        conn = mysql.connector.connect(host='localhost', user='root', password='password', database='mydatabase')
    except Error as E:
        click.echo(E)
    return conn


def create_table(conn, table_information):
    try:
        c = conn.cursor()
    #    c.execute('pragma journal_mode=wal;')
        c.execute(table_information)
    except Error as e:
        click.echo(e)


def db_query(statement):
    # start = time.time()
    database = r"mydatabase"
    query_conn = new_db_connection()
    with query_conn:
        cur = query_conn.cursor()
    #    cur.execute('pragma journal_mode=wal;')
     #   cur.execute('pragma cache_size=-10000;')
    #    cur.execute('PRAGMA synchronous = OFF')
    #    cur.execute('pragma threads=4')
        cur.execute(statement)
########
########
#THINK WE NEED conn.commit()
################
        data = cur.fetchall()
        # end = time.time()
        # total = end - start
    query_conn.close()
    # click.echo("Sql Query took: {} seconds".format(total))
    return data


def get_last_update_id():
    #database = r"mydatabase"
    conn = new_db_connection()
    try:
        with conn:
            cur = conn.cursor()
            sql = "SELECT update_id from diff"
            #cur.execute("SELECT update_id from diff;")
            cur.execute(sql)
            print(sql)
            data = cur.fetchall()
            print(data)
            new_id = len(data) + 1
            print(new_id)
    except Error:
        new_id = 1
    return new_id
#get_last_update_id()

def insert_update_info(conn, diff):
    sql = '''INSERT IGNORE into diff(update_id, timestamp, days, update_type, exid) VALUES(%s,%s,%s,%s,%s)'''
    cur = conn.cursor()
    #cur.execute('pragma journal_mode=wal;')
    cur.execute(sql, diff)
    conn.commit()

#def insert_update_info():
#    conn = mysql.connector.connect(host='localhost', user='root', password='password', database='mydatabase')

#    sql = '''INSERT IGNORE into diff(update_id, timestamp, days, update_type, exid) VALUES(%s,%s,%s,%s,%s)'''
#    #val = diff
#    diff = [14, str('hi'), str(4), "Vuln update", str(3424)]
#    cur = conn.cursor()
    #cur.execute('pragma journal_mode=wal;')
#    cur.execute(sql, diff)
#    conn.commit()
#insert_update_info()

def insert_compliance(conn, compliance):
    sql = '''INSERT IGNORE into compliance(asset_uuid, actual_value, audit_file, check_id, check_info, check_name, 
                    expected_value, first_seen, last_seen, plugin_id, reference, see_also, solution, status) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
    cur = conn.cursor()
  #  cur.execute('pragma journal_mod=wal;')
    cur.execute(sql, compliance)
    conn.committ()

def insert_assets(conn, assets):
    sql = '''INSERT IGNORE into assets(ip_address, hostname, fqdn, uuid, first_found, last_found, operating_system,
                       mac_address, agent_uuid, last_licensed_scan_date, network, acr, aes, aws_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
    cur = conn.cursor()
 #   cur.execute('pragma journal_mode=wal;')
    cur.execute(sql, assets)
    conn.commit()


def insert_tags(conn, tags):
    sql = '''INSERT IGNORE into tags(tag_id, asset_uuid, asset_ip, tag_key, tag_uuid, tag_value, tag_added_date) VALUES(%s,%s,%s,%s,%s,%s,%s)'''
    cur = conn.cursor()
 #   cur.execute('pragma journal_mode=wal;')
    cur.execute(sql, tags)
    conn.commit()


#def drop_tables(conn, table):
def drop_tables(table):
   # 
   
    conn = new_db_connection()
    try:
        with conn:
            drop_table = '''DROP TABLE {}'''.format(table)
            cur = conn.cursor()
            cur.execute(drop_table)
    except Error:
        pass
    

def insert_vulns(conn, vulns):
    sql = '''INSERT IGNORE into vulns(
                            asset_ip, 
                            asset_uuid, 
                            asset_hostname, 
                            first_found, 
                            last_found, 
                            output, 
                            plugin_id, 
                            plugin_name, 
                            plugin_family, 
                            port, 
                            protocol, 
                            severity, 
                            scan_completed, 
                            scan_started, 
                            scan_uuid, 
                            schedule_id, 
                            state,
                            cves,
                            score,
                            exploit
    ) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''

    cur = conn.cursor()
#    cur.execute('pragma journal_mode=wal;')
    cur.execute(sql, vulns)
    conn.commit()


def insert_apps(conn, apps):
    sql = '''INSERT IGNORE into apps(
             name,
             uuid, 
             target, 
             scan_completed_time,
             pages_audited,
             pages_crawled,
             requests_made, 
             critical_count,
             high_count,
             medium_count,
             low_count, 
             info_count,
             owasp,
             tech_list,
             config_id)
     VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
    cur = conn.cursor()
# #   cur.execute('pragma journal_mode=wal;')
    cur.execute(sql, apps)
    conn.commit()