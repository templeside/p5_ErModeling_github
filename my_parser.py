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

"from dict, return to a formatted string"
def dict_to_sentence(order_list, val_dict):
    string = ""
    for order in order_list:
        string += val_dict[order] +"|" if(val_dict[order] !=None) else "NULL" +"|"
    result = string[:-1]+"\n"
    return result


"from list, return to a formatted string"
def list_to_sentence(orders):
    string = ""
    for order in orders:
        string += order +"|"
    result = string[:-1]+"\n"

    return result

"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""
def parseJson(json_file):
    # based on the .dat files
    items_oders= ['ItemID', 'Name','Currently', 'Buy_Price', 'First_Bid',  'Number_of_Bids', 'Started', 'Ends','Description', 'Seller']
    users_visited= set() # for duplication checker #TODO: figure out to check duplication or adding location and country

    # opening the .dat files and json files
    with open(json_file, 'r') as f, open('category.dat', 'a') as category_dat, open('items.dat', 'a') as items_dat, open('users.dat', 'a') as users_dat, open('bids.dat', 'a') as bids_dat:
        items = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file
    
        for item in items:
            """
            TODO: traverse the items dictionary to extract information from the
            given `json_file' and generate the necessary .dat files to generate
            the SQL tables based on your relation design
            """
            #found requirements and non requirements, transform date and dollar format.
            items_vals={}

            #string vals or dat.write()
            users_str=""
            category_str=""
            bids_str=""          #String Dictionary. several bid histories

        
            ## for items.dat && users.dat && bids.dat
            for attr in items_oders:
                if(attr=='Currently' or attr=='First_Bid'):
                    items_vals[attr] = transformDollar(item[attr])
                
                elif(attr=="Started" or attr =="Ends"):  #when transformed to preferred date format
                    items_vals[attr] = transformDttm(item[attr])
                    
                elif(attr=="Seller"):
                    sellerInfo= item[attr]  # sellerInfo = ["UserID", "Rating"]
                    items_vals[attr] = sellerInfo["UserID"]
                    #for sellers in users.dat
                    if(not sellerInfo["UserID"] in users_visited):  # adding to 
                        users_str += list_to_sentence([sellerInfo["UserID"],sellerInfo["Rating"],item["Country"],item["Location"]])                            
                        users_visited.add(sellerInfo["UserID"])
                        
                elif(attr=='Buy_Price'): 
                    #When no bid
                    if(attr in item):
                        items_vals[attr] = transformDollar(item[attr])
                    else:
                        items_vals[attr] = "NULL"
                        
                else: #for ItemID, Name, Description, Number of bid
                    items_vals[attr] = item[attr]

            #for bid.dat, bidder history
            if("Bids" in item and item["Bids"] !=None):
                bids_list = item["Bids"]
                for bid in bids_list:
                    bid_attr = bid["Bid"] #bid_attr.keys() = (['Bidder', 'Time', 'Amount'])                                
                    bidder_info = bid_attr["Bidder"]

                    bids_str += list_to_sentence([item["ItemID"], bidder_info["UserID"], bid_attr["Time"],transformDollar(bid_attr["Amount"])])
            
                    #for users.dat, bidder user 
                    bidder_id = bidder_info["UserID"]
                    bidder_rate = bidder_info["Rating"]
                    bidder_country = "NULL" if not"Country" in bidder_info else bidder_info["Country"]
                    bidder_location = "NULL" if not"Location" in bidder_info else bidder_info["Location"]
                    
                    users_str += list_to_sentence([bidder_id, bidder_rate, bidder_country, bidder_location]) 
                    users_visited.add(bidder_id)
            ## for category.dat
            category_attr = item["Category"]
            for attr in category_attr:
                category_str+= list_to_sentence([item["ItemID"],attr])

            #saving to the files.
            category_dat.write(category_str)
            items_dat.write(dict_to_sentence( items_oders, items_vals))
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
    # main([0,"items-0.json"])
    main(sys.argv)