# -*- coding:utf-8 -*-

__author__ = "Chanhee Lee"
_id_number_ = 12111613
from func_lib import *
import math
import MySQLdb as mdb

#
#   DB connect ID / PW
#
host_ = "localhost"
port_ = 6304
user_ = "root"
database_ = "probablity"
ps_ = "lg29186t"
E_ = math.e



# get total data
def get_total():
    global host_, port_, user_, database_, ps_
    db = mdb.connect(host=host_, port=port_, user=user_, db=database_, passwd=ps_)
    cur = db.cursor()
    cur.execute("set names utf8")
    sql = "select TH,TI from total where name= 11"
    cur.execute(sql)
    l_data = cur.fetchone()

    return l_data # [0] : TH [1] : TI

# reset function
def total_reset():
    global host_, port_, user_, database_, ps_
    db = mdb.connect(host=host_, port=port_, user=user_, db=database_, passwd=ps_)
    cur = db.cursor()
    sql = 'update total set TH=0,TI=0 where name = 11'
    cur.execute(sql)
    db.commit()

# reseet function
def pro_reset():
    global host_, port_, user_, database_, ps_
    db = mdb.connect(host=host_, port=port_, user=user_, db=database_, passwd=ps_)
    cur = db.cursor()
    sql = 'delete from pro where true'
    cur.execute(sql)
    db.commit()

# total count update function for practicing
def total_update(site_type):
    global host_, port_, user_, database_, ps_
    db = mdb.connect(host=host_, port=port_, user=user_, db=database_, passwd=ps_)
    cur = db.cursor()
    cur.execute("set names utf8")
    # 0 -> general 1-> harmful
    if site_type == 0:
        sql = 'call probablity.total_update(0);'
        cur.execute(sql)
        db.commit()
    else:
        sql = 'call probablity.total_update(1);'
        cur.execute(sql)
        db.commit()

# get probablity
def get_probablity(word_):
    global host_, port_, user_, database_, ps_
    db = mdb.connect(host=host_, port=port_, user=user_, db=database_, passwd=ps_)
    cur = db.cursor()
    cur.execute("set names utf8")
    sql = "select * from pro where word = (%s)"
    cur.execute(sql, (str(word_),))
    L = cur.fetchone()
    if L == None:
        return 0.25
    else:
        return L[1]

# update probablity and count
def word_update(word_,num ,site_type):
    # word_ : keyword
    # num : number of keyword
    # site_type : harmful or general?

    global host_, port_, user_, database_, ps_
    db = mdb.connect(host=host_, port=port_, user=user_, db=database_, passwd=ps_)
    cur = db.cursor()
    cur.execute("set names utf8")

    sql = "select * from pro where word = (%s)"
    cur.execute(sql,str(word_))
    L = cur.fetchone()
    if  L == None:
        # there is no data
        # so insert new one
        sql = "insert into pro values(%s,0.25,0,%s)"
        if site_type == 0:
            # if it is general site
            cur.execute(sql,(str(word_), str(num),))
            db.commit()
        else:
            sql = "insert into pro values(%s,0.5, %s, 0)"
            # if it is harmful site
            cur.execute(sql, (str(word_), str(num),))
            db.commit()

    else:
        # existed data
        # fetch data

        cinh = L[2]
        cing = L[3]


        # get Total data
        l_data = get_total()
        TH = int(l_data[0])
        TI = int(l_data[1])



        if site_type == 0:
            #general site
            # calculate new probablity
            cing += num
            new_p = 0.0

            if TH != 0:
                new_p = (float(cinh) / float(TH)) + (float(cing) / float(TI))
                new_p = (float(cinh) / float(TH)) / new_p

            if new_p == 0.0:
                new_p = 0.25

            elif new_p == 1.0:
                new_p = 0.99


            # update probablity , cing
            sql = "update pro set Probablity = %s , CinG = %s where word = %s"
            cur.execute(sql,(str(new_p),str(cing),str(word_),))
            db.commit()

        else:
            # harmful site
            # calculate new probablity
            cinh += num
            new_p = 0.0

            if TI!=0:
                new_p = float((float(cinh) / float(TH)) + (float(cing) / float(TI)))
                new_p = (float(cinh)/float(TH)) / new_p

            if new_p == 0.0:
                new_p = 0.25

            elif new_p == 1.0:
                new_p = 0.99


            # update probablity , cinh
            sql = "update pro set Probablity = %s , CinH = %s where word = %s"
            cur.execute(sql, (str(new_p), str(cinh), str(word_),))
            db.commit()



# THIS IS TRAINING FUNCTION
# input -> URL , type
# result -> calculate word's harmful probability

def training(url,site_type):



    if site_type == 0:
        # general site type
        # total update
        total_update(0)

        # and connect url
        # it is Cho's part
        # crawling and tokenizing the words
        dic = crw(url)
        for i in dic:
            word_update(i,1,0)

    else:
        # harmful site type
        # total update
        total_update(1)

        dic = crw(url)
        for i in dic:
            word_update(i, 1, 1)


# decision module
def decision(list):
    global E_

    answer = 0.0
    p1 = 0.0
    p2 = 0.0
    count_all = 0.0
    count_harm = 0.0

    #t = get_total()

    for word in list:
        # receive probability
        pp = get_probablity(word)
        # calculate
        # set log protecting for underflow
        if pp >= 0.7:
            count_harm +=1.0

        print "Word : %s , Probability : %f" %(word , pp)

        count_all += 1.0
        p1 += math.log(pp)
        p2 += math.log(1.0 - pp)

    p2 = p2 - p1
    print p2

    try:
        p2 = pow(E_,p2)
        answer = (1.0/(1.0 + p2)) * 100.0

    except OverflowError:
        return 0.0

    except ZeroDivisionError:
        print "There is no word so, i can't decide!!"
        return -1

    return answer







