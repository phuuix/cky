''' stockbase.py '''
import os
import time
import tushare as ts
import numpy as np
from pandas import Series, DataFrame

def initbase():
	# set tonglian token
	ts.set_token('358e98ec17002e901308c16ea71188ca7a55984379feca7dd3bab072acd502d3')
	return

class FileNameConst:
	basics = 0
	assetdebt = 1
	cashflow = 2
	profit = 3
	history = 4
	industry = 5

class StockConst:
	start_year = 2007
	
def stock_build_fname(name_const, tickerId=''):
	if name_const == FileNameConst.basics:
		filename = "stock_basics.csv"
	elif name_const == FileNameConst.assetdebt:
		filename = "assetdebt_"+tickerId+'.csv'
	elif name_const == FileNameConst.profit:
		filename = "profit_"+tickerId+'.csv'
	elif name_const == FileNameConst.cashflow:
		filename = "cashflow_"+tickerId+'.csv'
	elif name_const == FileNameConst.history:
		filename = "history_"+tickerId+'.csv'
	elif name_const == FileNameConst.industry:
		filename = "stock_industry.csv"
	else:
		filename = None
	return filename
	
def update_stock_basics(path="", forced=True):
	''' 
	Brief: 更新上市公司基本情况到本地
	'''
	filename = stock_build_fname(FileNameConst.basics, '')
	if os.path.exists(filename) == False or forced == True:
		df = ts.get_stock_basics()
		if df is not None:
			df.to_csv(path+stock_build_fname(FileNameConst.basics, ""), encoding='utf-8')
	return df

def update_stock_industry(path="", forced=False):
	'''
	Brief: 更新行业列表
	'''
	filename = stock_build_fname(FileNameConst.instusry)
	if os.path.exists(filename) == False or forced == True:
		df = ts.get_industry_classified()
		if df is not None:
			df.to_csv(filename, encoding='utf-8')
	return df
			
def update_stock_hist_one(tickerId, path=""):
	market = ts.Market()
	
	# 更新资产负债表
	filename = path+stock_build_fname(FileNameConst.history, tickerId)
	if os.path.exists(filename) == False:
		df = market.MktEqud(ticker=tickerId)
		if df is not None:
			df.to_csv(filename, encoding='utf-8')
	else:
		print('file existed: '+filename+'\n')

def update_stock_hist_all(path=""):
	'''
	Brief: 更新所有上市公司的日k线（Tushare通联接口）
	'''
	# 更新股票列表和基本信息
	print('update stock history\n')
	basics = update_stock_basics(path)
	
	for tickerId in basics.index:
		print('update history: '+tickerId+'\n')
		update_stock_hist_one(tickerId, path)
	return

	'''
		df_old = DataFrame.from_csv(filename)
		lastDate = df_old['endDate'].max
		# more quarters need to update?
		localtime = time.localtime(time.time())
		df = bd.FdmtBS(ticker=tickerId, beginDate=, endDate=)
		df_old.append(df)
		df.to_csv(filename, encoding='utf-8')
	'''
	
def update_stock_basics_one(tickerId, path=""):
	'''
	更新一家上市公司的报表信息
	'''
	bd = ts.Fundamental()
	
	# 更新资产负债表
	filename = path+stock_build_fname(FileNameConst.assetdebt, tickerId)
	if os.path.exists(filename) == False:
		df = bd.FdmtBS(ticker=tickerId)
		df.to_csv(filename, encoding='utf-8')
	else:
		print('file existed: '+filename+'\n')
		
	# 更新现金流量表
	filename = path+stock_build_fname(FileNameConst.cashflow, tickerId)
	if os.path.exists(filename) == False:
		df = bd.FdmtCF(ticker=tickerId)
		df.to_csv(filename, encoding='utf-8')
	else:
		print('file existed: '+filename+'\n')
		
	# 更新利润表
	filename = path+stock_build_fname(FileNameConst.profit, tickerId)
	if os.path.exists(filename) == False:
		df = bd.FdmtIS(ticker=tickerId)
		df.to_csv(filename, encoding='utf-8')
	else:
		print('file existed: '+filename+'\n')
	
def update_stock_basics_all(path=""):
	'''
	Brief: 更新所有上市公司的报表（Tushare通联接口）
	'''
	# 更新股票列表和基本信息
	print('update stock list\n')
	basics = update_stock_basics(path)
	
	for tickerId in basics.index:
		print('update basics: '+tickerId+'\n')
		update_stock_basics_one(tickerId, path)
	
def build_stock_basics_allinone(path="", forced=False):
	'''
	Brief: build基本面数据大表
	Return:
		code,代码
		name,名称
		report_date,发布日期
		eps,每股收益
		bvps,每股净资产
		roe,净资产收益率(%)
		epcf,每股现金流量(元)
		net_profits,净利润(万元)
		profits_yoy,净利润同比(%)
		net_profit_ratio,净利率(%)
		gross_profit_rate,毛利率(%)
		business_income,营业收入(百万元)
		mbrg,主营业务收入增长率(%)
		arturnover,应收账款周转率(次)
		arturndays,应收账款周转天数(天)
		inventory_turnover,存货周转率(次)
		inventory_days,存货周转天数(天)
		currentasset_turnover,流动资产周转率(次)
		currentasset_days,流动资产周转天数(天)
		totals,总股本(万)
	'''
	# update local tables
	
	print ("start to build basic allinone table...")
	localtime = time.localtime(time.time())
	for year in range(StockConst.start_year,localtime.tm_year):
		# build filename
		filename = path+"stock_basics_allinone"+str(year)+'_'+str(quarter)+'.csv'
		if (os.path.exists(filename) == False) or (forced == true):
			# build allinone DataFrame
			df_allinone = DataFrame(columns=['code', 'name', 'report_date', 'eps', 'roe', 'epcf', 'net_profits', 'profits_yoy', \
			'net_profit_ratio', 'gross_profit_rate', 'business_income', 'mbrg', 'arturnover', 'arturndays', 'inventory_turnover', \
			'inventory_days', 'currentasset_turnover', 'currentasset_days', 'totals'])
		
			# build 
			#for code in df_report['code'].values:
			#	df_allinone.ix[]
				
	
	print ("done")
	return
##########################################################################
def get_top_basic(year, quarter, nMax, field, max_or_min):
	''' 返回如最大或最小PE/PB/ROE
	'''
	return

def get_basic_data(code, year, quarter):
	return

###########################################################################
def update_intustry_basic(intustry_code):
	''' 更新行业基本数据
	'''
	return

def update_intustry_index():
	''' 更新行业指数 (day)
	'''
	
	return

#############################################################################
def top_pe():
	return

def top_pb():
	return

def top_market_value():
	return
	
def top_changeup():
	return
	
def top_changedown():
	return
