# stock technical analysis 
import tushare as ts
import numpy as np

def normalizeLine(line):
	''' Normalize a line
		line: input, type numpy.ndarray
		return: a new line normalized
	'''
	if (line[0] != 0):
		newline = line/line[0]
	else:
		newline = np.array(())
	return newline

def derivationLine(line):
	''' derivation of a line
		line: input, type numpy.ndarray
		return: a new line after derivation
	'''
	
	length = line.size
	newline = np.zeros(length)
	for i in range(1, length):
		newline[i] = line[i] - line[i-1]
	
	# copy the 2nd to 1st point 
	newline[0] = newline[1]
	
	return newline
	
def moveAverageSeries(x, avgPoint):
	''' move average filter
		x numpy.ndarray: input series
		avgPoint: number of point to be averaged
		return: a new line after filter
	'''
	N = x.size - avgPoint
	if (N > 0):
		y = np.zeros(N)
		y[0] = x[0:avgPoint].sum
		for n in range(1, N):
			y[n] = (y[n-1] + x[n+N-1] - x[n-1])/N
		
		return y
	else:
		return None

def betaFilterSeries(x, beta, y_minus1=0):
	'''
	Brief
		y[-1] = y_minus1;
		y[n] = y[n-1]*beta + x[n]*(1-beta)     n>=0
	Parameters
		x numpy.ndarray: series to be filtered
		y_minus1: initial values
		beta: filter factor
	Return
		y
	'''
	y = np.zeros(x.size)
	y[0] = (y_minus1 - x[0])*beta + x[0]
	for n in range(1, x.size):
		y[n] = (y[n-1]-x[n])*beta + x[n]
	
	return y

def adx(x):
	return
	
def KDJ(x, nDay=9):
	'''
	Brief
		K[-1] = 50; D[-1] = 50
		RSV[n] = (Close[n]-Lowest9(n))/(Highest9(n)-Lowest9(n))*100
		K[n] = 2/3*K[n-1] + 1/3*RSV[n]
		D[n] = 2/3*D[n-1] + 1/3*K[n]
		J[n] = 3*K[n] - 2*D[n]
	'''
	
	length = x.size;
	if (length >= nDay) and (nDay > 0):
		K = np.zeros(length-nDay)
		D = np.zeros(length-nDay)
		J = np.zeros(length-nDay)
		
		# calculate the first element of K & D & J
		min_v = x[0:nDay].min()
		max_v = x[0:nDay].max()
		rsv = (x[nDay-1]-min_v)/(max_v-min_v)*100
		K[0] = 2/3*50 + 1/3*rsv
		D[0] = 2/3*50 + 1/3*K[0]
		J[0] = 3*K[0] - 2*D[0]
		
		# calculate other elements
		for n in range(1, length-nDay):
			min_v = x[n:n+nDay].min()
			max_v = x[n:n+nDay].max()
			rsv = (x[n+nDay-1]-min_v)/(max_v-min_v)*100
			K[n] = 2/3*K[n-1] + 1/3*rsv
			D[n] = 2/3*D[n-1] + 1/3*K[n]
			J[n] = 3*K[n] - 2*D[n]

		return (K, D, J)
	else:
		return None

def MACD(x, t1=12, t2=26, t3=10):
	'''
	Brief
		init: EMA12=EMA26=DIFF=DEA=BAR=0
		EMA12[n] = EMA12[n-1]*11/13 + Close[n]*2/13
		EMA26[n] = EMA26[n-1]*25/27 + Close[n]*2/27
		DIF[n] = EMA12[n] - EMA26[n]
		DEA[n] = DEA[n-1]*8/10 + DIF[n]*2/10
		BAR[n] = 2*(DIF[n] - DEA[n])
	Parameters
		x: serires of Close price
		t1: average period of EMA1
		t2: average period of EMA26
		t3: avearge period of DEA
	Return:
		DIF, DEA, BAR
	'''
	ema1 = betaFilterSeries(x, (t1-1)/(t1+1), x[0])
	ema2 = betaFilterSeries(x, (t2-1)/(t2+1), x[0])
	dif = ema1 - ema2
	dea = betaFilterSeries(dif, (t3-1)/(t3+1), dif[0])
	bar = 2*(dif-dea)
	return (dif, dea, bar)

def RSI(x, nDay=14):
	'''
	Brief
		RSI = 100*sum(changes > 0 in nDay)/sum(changes in nDay)
	'''
	length = x.size;
	if (length >= nDay) and (nDay > 0):
		rsi = np.zeros(length-nDay)
		for i in range(0, rsi.size):
			sum_up = 0
			sum_down = 0
			
			for n in range(0, nDay):
				if x[i+n] > 0:
					sum_up += x[i+n]
				else:
					sum_down -= x[i+n]
					
			rsi[i]=100*sum_up/(sum_up+sum_down)
		return rsi
	else:
		return None

def lineTrendLs(S):
	''' 
	Brief
		Least squares polynomial fit (1D): s = a + b*x
	Parameters
	Return
		[b a]
	'''
	x = np.arange(0, S.size)
	z = np.polyfit(x, S, 1)
	# fetch the new data
	# p = np.poly1d(z)
	# y = p(x)
	
	return z

def lineTrendMle(S):
	''' 
	Brief
		fit 1D line by Maximum Likelyhood Estimation: s = a + b*x
	Parameters
		S: numpy.ndarray
	Return
		[b, a]
	'''
	N = S.size
	x = np.arange(0, N)
	b = (np.dot(x, S)-(N-1)/2*S.sum())/((N-1)*N*(N+1)/12)
	a = (S.sum() - b * N*(N-1)/2)/N
	return [b, a]

def industryIndex():
	return

