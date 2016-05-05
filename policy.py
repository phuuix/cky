''' policy.py '''

from stockbase.py import *
from techanalysis.py import *

def evaluate_rebanlance_period(rebanlance_period, day):
	ret = False
	if day[0] == rebanlance_period:
		ret = True
		day[0] = 1
	else:
		day[0] = day[0] + 1
	
	return ret

def policy_min_capital(start_date, end_date, rebanlance_period):
	''' 
	Brief: 最小市值策略，选取最小市值并且不亏损的8只股票
	'''
	global securityBasic
	n = [rebanlance_period]
	date = start_date
	while date < end_date:
		if not is_trade_date(date):
			date = next_day()
			continue
		
		if evaluate_rebanlance_period(rebanlance_period, n):
			list = top_market_value(date, 100)
			''' choose the stock '''
			for stock in list:
		
		date = next_day()

			
def policy_best_metric(start_date, end_date, rebanlance_period):
	'''
	Brief: 最佳
	'''

def policy_vote_system()
	return
	
