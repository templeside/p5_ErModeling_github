"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS564 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import loads
from re import sub

columnSeparator = "|"

items_orders= ['ItemID', 'Name','Currently', 'Buy_Price', 'First_Bid',  'Number_of_Bids', 'Started', 'Ends','Description', 'Seller']
users_visited= set()
bidID=0

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)


def add_user(userID,Rating,Location,Country):
    #userID already parsed
    to_add = ""
    to_add+=userID
    to_add+=columnSeparator
    to_add+=Rating
    to_add+=columnSeparator
    if Location=="NULL":
        to_add+=Location
    else:
        to_add+=escape_string(Location)
    to_add+=columnSeparator
    if Country=="NULL":
        to_add+=Country
    else:
        to_add+=escape_string(Country)
    return to_add+"\n"

def add_bid(bidID,itemID,userID,Time,Amount):
    to_add = ""
    to_add+=str(bidID)
    to_add+=columnSeparator
    to_add+=itemID
    to_add+=columnSeparator
    to_add+=userID
    to_add+=columnSeparator
    to_add+=Time
    to_add+=columnSeparator
    to_add+=Amount
    return to_add+"\n"



def escape_string(line):
    if line==None:
        return "NULL"
    line = line.strip()
    new_line = "\""
    for a in line:
        new_line+=a
        if a=="\"":
            new_line+="\""
    new_line+="\""
    return new_line

"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""
def parseJson(json_file):
    global bidID

    # opening the .dat files and json files
    with open(json_file, 'r') as f, open('category.dat', 'a') as category_dat, open('items.dat', 'a') as items_dat, open('users.dat', 'a') as users_dat, open('bids.dat', 'a') as bids_dat:
        items = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file

        for item in items:
            """
            TODO: traverse the items dictionary to extract information from the
            given `json_file' and generate the necessary .dat files to generate
            the SQL tables based on your relation design
            """

            items_vals={}
            users_str=""
            category_str=""
            bids_str=""

        
            ## for items.dat
            for attr in items_orders:
                if(attr=='Currently' or attr=='First_Bid'):
                    items_vals[attr] = transformDollar(item[attr])
                
                elif(attr=="Started" or attr =="Ends"):  
                    items_vals[attr] = transformDttm(item[attr])
                    
                elif(attr=="Seller"):
                    sellerInfo= item[attr]  # sellerInfo = ["UserID", "Rating"]
                    good_userID = escape_string(sellerInfo["UserID"])
                    items_vals[attr] = good_userID
                    #for sellers in users.dat
                    if(not good_userID in users_visited):  # adding to 
                        users_str += add_user(good_userID,sellerInfo["Rating"],item["Country"],item["Location"])                            
                        users_visited.add(good_userID)
                        
                elif(attr=='Buy_Price'): 
                    #when it's not set
                    if(attr in item):
                        items_vals[attr] = transformDollar(item[attr])
                    else:
                        items_vals[attr] = -1
                
                elif ((attr=="Description")|(attr=="Name")):
                    items_vals[attr] = escape_string(item[attr])
                        
                else: #for ItemID, Number of bid
                    items_vals[attr] = item[attr]

            #for bid.dat, bidder history
            if(item["Bids"] !=None):
                bids_list = item["Bids"]
                for bid in bids_list:
                    bid_attr = bid["Bid"] #bid_attr.keys() = (['Bidder', 'Time', 'Amount'])                                
                    bidder_info = bid_attr["Bidder"]
                    good_bidderID = escape_string(bidder_info["UserID"])
                    bids_str += add_bid(bidID, item["ItemID"], good_bidderID, bid_attr["Time"],transformDollar(bid_attr["Amount"]))
            
                    #for users.dat, bidder user 
                    if "Country" not in bidder_info:
                        bidder_info["Country"] = "NULL"
                    if "Location" not in bidder_info:
                        bidder_info["Location"] = "NULL"
                    users_str += add_user(good_bidderID, bidder_info["Rating"], bidder_info["Country"], bidder_info["Location"]) 
                    users_visited.add(good_bidderID)
                    bidID+=1

            ## for category.dat
            category_attr = item["Category"]
            cat_set = set()
            for cat in category_attr:
                if cat in cat_set:
                    continue
                category_str+= item["ItemID"]+columnSeparator+escape_string(cat)+"\n"

            #saving to the files.
            category_dat.write(category_str)
            items_dat.write(columnSeparator.join(str(items_vals[key]) for key in items_orders)+"\n")
            users_dat.write(users_str)
            bids_dat.write(bids_str)   
            

"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print ("Success parsing " + f)
            
if __name__ == '__main__':
    main(sys.argv)