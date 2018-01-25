from function import *
from func_lib import *
from TwitterC import *
import time

MY_OWN_ID = 794856483007533057
HARM_USER_ID = 4872154028


def main():

    while True:
        print "Welcome to the Site Judgement System"
        print "Choose the options"
        print "1. training site"
        print "2. judge the site"
        print "3. reset DB"
        print "4. exit"

        num = int(input("Input number : "))

        if num == 1:

            site_type = int(raw_input("Site type ?(general : 0 , harmful : 1 , twitter : 2) : "))

            if site_type == 0:

                file_ = "general.txt"
                f1 = open(file_,"r")

                print "Training general site"
                while True:
                    addr = f1.readline()
                    if not addr:
                        break

                    # training the general site
                    print "training site : %s" % (addr)
                    training(addr, 0)
                f1.close()


            elif site_type == 2:
                print "Crawling the twitter"
                # crawling twitter

                site_t = int(raw_input("site type : ?"))

                if site_t == 1:
                    id = HARM_USER_ID
                else:
                    id = MY_OWN_ID
                # if raise Error ... sleep 15minutes
                try:
                    flist = []
                    twitterC(id,flist,site_t)
                except tweepy.TweepError:
                    print "Sleep 15min............."
                    time.sleep(60 * 15)
                    continue
                except StopIteration:
                    break

                # bfs searching the friends
                for i in flist:
                    try:
                        twitterC(i,flist,site_t)
                        flist.remove(i)
                    except tweepy.TweepError:
                        print "Sleep 15min................"
                        time.sleep(60 * 15)
                        continue
                    except StopIteration:
                        break

            else:

                file_ = "harmful.txt"
                f2 = open(file_, "r")

                # training the harmful site
                print "Training harmfulsite..."
                while True:
                    addr = f2.readline()
                    if not addr:
                        break

                    print "training site : %s" % (addr)
                    training(addr, 1)

                f2.close()


        elif num==2:
            # judge the site
            print "judge the site probability"
            url = raw_input("input url : ")
            probability = decision(crw(url))
            #ddd(crw(url))
            print "%2f%%" %(probability)

        elif num==3:
            # reset the db
            # reset total data
            print "Are you sure reset the DB???? yes/no"
            answer = raw_input()
            if answer == 'yes':
                print "reset...."
                total_reset()
                # reset probability data
                pro_reset()
                print "Data reset complete"
            else:
                pass


        elif num==4:
            print "bye"
            break



main()