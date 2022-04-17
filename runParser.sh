rm *.dat
rm *.db
python3 my_parser.py ebay_data/items-*.json
sqlite3 auction.db < load.txt
sqlite3 auction.db < query1.sql
sqlite3 auction.db < query2.sql
sqlite3 auction.db < query3.sql
sqlite3 auction.db < query4.sql
sqlite3 auction.db < query5.sql
sqlite3 auction.db < query6.sql
sqlite3 auction.db < query7.sql