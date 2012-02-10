import sqlite3, locale, urllib2
try:
    locale.setlocale(locale.LC_ALL, 'English_United States')
except:
    locale.setlocale(locale.LC_ALL, 'en_US.utf8')

def portfolio(self, e):
	
	args = e.input.upper().split()
	nick = e.nick.upper()
	
		
	if len(args) == 4:		# arguments for adding stock
		command,stock,numshares,pricepaid = args
		if command != "ADD":
			return
		
		e.source = e.nick
		e.notice = True
		e.output = add_stock(nick, stock, numshares, pricepaid)
		return e
			
		
	elif len(args) == 2:	# arguments for deleting stock
		command,stock_rowid = args
		if command != "DEL":
			return
			
		e.source = e.nick		
		e.notice = True
		e.output = del_stock(nick, stock_rowid)
		return e
		
	elif len(args) == 1:	# argument for listing portfolio
		command = args[0]
		if command != "LIST":
			return
		e.source = e.nick
		e.notice = True
		e.output = list_stock(nick)
		
	elif len(args) == 0:
		e.output = get_stocks(nick)
		return e

		
	
	return e

def add_stock(nick,stock,numshares,pricepaid):
	conn = sqlite3.connect('portfolios.sqlite')
	c = conn.cursor()
	result = c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='portfolios';").fetchone()
	if not result:
		c.execute('''create table portfolios(user text, stock text, numshares integer, pricepaid real)''')
	
	try:
		numshares = int(numshares)
		pricepaid = float(pricepaid)
	except:
		return "Please use the correct command to add stocks to your portfolio."
	
	c.execute("INSERT INTO portfolios VALUES (?,?,?,?)", [nick,stock,numshares,pricepaid])
	conn.commit()
	conn.close()
	
	return "Added %s shares of %s at $%s." % (numshares, stock, pricepaid)

def del_stock(nick, stock_rowid):
	conn = sqlite3.connect('portfolios.sqlite')
	c = conn.cursor()
	result = c.execute("DELETE FROM portfolios WHERE user = ? AND rowid = ?", [nick, stock_rowid]).rowcount
	conn.commit()
	conn.close()
	
	if result == 0:
			return "You did something wrong, try again."
	if result == 1:
			return "Deleted portfolio entry #%s" % (stock_rowid)
	

def list_stock(nick):
	stocks = []
	id_counter=0
	
	conn = sqlite3.connect('portfolios.sqlite')
	c = conn.cursor()
	try:
		result = c.execute("SELECT rowid, stock, numshares, pricepaid FROM portfolios WHERE user = ?", [nick]).fetchall()
	except:
		return "You're too poor to own stock."
		
	
	conn.close()
	
	return_line="ID%s%s%s\n" % ("Symbol".center(10),"# of Shares".center(15),"Price Paid".center(12), "Current Price")
	
	if result:
		for stock in result:
			stocks.append(stock[1])
		
		stock_prices = get_stocks_prices(stocks)

		
		for stock in result:
			return_line += "%s%s%s%s%s\n" % (stock[0],stock[1].center(10),str(stock[2]).center(15),str(stock[3]).center(12),str(stock_prices[id_counter]).center(13))
			id_counter+=1
		return return_line
	else: 
		return "You're too poor to own stock."
	
def get_stocks_prices(stocks): ## pass in a list or tuple of stocks and get back their prices in a tuple
	opener = urllib2.build_opener()
	opener.addheaders = [('User-Agent',"Opera/9.10 (YourMom 8.0)")]
	
	stocks = "+".join(stocks)
	pagetmp = opener.open("http://download.finance.yahoo.com/d/quotes.csv?s=%s&f=l1" % stocks)
	quote = pagetmp.read(1024)

	return quote.split("\r\n")
      
	

portfolio.command = "!portfolio"
portfolio.helptext = "!portfolio help text"
