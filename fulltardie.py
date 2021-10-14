import os
from datetime import datetime
import calendar

cdr = os.path.split(os.path.realpath('fullardie.py'))[0]

def padstr(instr, pad, padlen) :
	dif = (padlen - len(instr)) + 1
	o = instr
	for i in range(1,dif) :
		o = o + pad
	return(o)

def prepadstr(instr, pad, padlen) :
	dif = (padlen - len(instr)) + 1
	o = ''
	for i in range(1,dif) :
		o = o + pad
	o = o + instr
	return(o)

def flatten(x) :
	if isinstance(x, list) :
		return [a for i in x for a in flatten(i)]
	else:
		return [x]

def prepret(y,m,d) :
	ds = prepadstr(str(d),'0',2)
	ms = prepadstr(str(m),'0',2)
	dn = (str(y)[2:] + prepadstr(str(m),'0',2) + ds)
	lds = (str(y) + '-' + ms + '-' + ds)
	return([dn,lds])


def getnth(title,calctype,nth,startdate,amt,enddate):
	n = datetime.now()
	nn = datetime.toordinal(n)
	if startdate == '' :
		dt = n
	else :
		dt = datetime.strptime(startdate,'%y%m%d')
	oo = datetime.toordinal(dt)
	et = datetime.strptime(enddate,'%y%m%d')
	ee = datetime.toordinal(et)
	pile = []

	
	if calctype == 'nthdayfromdate' :
		nthd = nth.split('.')[1]
		nthp = int(nth.split('.')[0])
		d = 0
		oo = datetime.toordinal(dt)
		for h in range(360) :
			if oo > nn :
				dt = datetime.fromordinal(oo)
				pile.append([prepret(dt.year,dt.month,dt.day),title,amt])
				if oo > ee : break
			oo = oo + (nthp * 7)
			
	if calctype == 'nthweekdayofmonth' :
		nthd = nth.split('.')[1]
		g = int(nth.split('.')[0])
		d = 0
		if nthd == 'monday' : d = 0
		if nthd == 'tuesday' : d = 1
		if nthd == 'wednesday' : d = 2
		if nthd == 'thursday' : d = 3
		if nthd == 'friday' : d = 4
		if nthd == 'saturday' : d = 5
		if nthd == 'sunday' : d = 6
		m = dt.month
		y = dt.year
		ld = calendar.monthrange(y,m)[1]
		for week in calendar.monthcalendar(y, m) :
			if week[d] != 0 : ld = min(ld, week[d])
		dt = dt.replace(y,m,ld)
		oo = datetime.toordinal(dt)
		while oo < ee :
			if oo > nn :
				dt = dt.fromordinal(oo)
				pile.append([prepret(dt.year,dt.month,dt.day),title,amt])			
			ld = ld + (g*7)
			remo = 0
			if ld > calendar.monthrange(y,m)[1] : m = m + 1; remo = 1
			if m > 12 :
				m = m % 12
				y = y + 1
				remo = 1
			if remo == 1 :
				ld = 99
				for week in calendar.monthcalendar(y, m) :
					if week[d] != 0 : ld = min(ld, week[d])
			dt = dt.replace(y,m,ld)
			oo = datetime.toordinal(dt)
				
	if calctype == 'monthly' :
		m = dt.month
		y = dt.year
		d = int(nth)
		while oo < ee :
			if m > 12 :
				m = m % 12
				y = y + 1
			dt = dt.replace(y,m,d)
			oo = datetime.toordinal(dt)
			if nn < oo :
				pile.append([prepret(dt.year,dt.month,dt.day),title,amt])
			m = m + 1
			
	if calctype == 'nthmonth' :
		m = dt.month
		y = dt.year
		d = dt.day
		while oo < ee :
			if m > 12 :
				m = m %12
				y = y + 1
			dt = dt.replace(y,m,d)
			oo = datetime.toordinal(dt)
			if nn < oo :
				pile.append([prepret(dt.year,dt.month,dt.day),title,amt])
			m = (m + d)

	if calctype == 'dayly' :
		d = int(nth)
		while oo < ee :
			oo = oo + d
			if nn < oo :
				dt = datetime.fromordinal(oo)
				pile.append([prepret(dt.year,dt.month,dt.day),title,amt])
				
	if calctype == 'dateofnthmonthfromdate' :
		m = dt.month
		y = dt.year
		nthmonth = int(nth.split('.')[0])
		d = int(nth.split('.')[1])
		c = 1
		while oo < ee :
			if m > 12 :
				m = (m - 12)
				y = (y + 1)
			dt = dt.replace(y,m,d)
			oo = datetime.toordinal(dt)
			if oo > nn :
				pile.append([prepret(dt.year,dt.month,dt.day),title,amt])
			m = m + nthmonth
			
	if calctype == 'getfirstorlastweekdayofmonth' :
		nthd = nth.split('.')[0]
		g = nth.split('.')[1]
		d = 0
		if nthd == 'monday' : d = 0
		if nthd == 'tuesday' : d = 1
		if nthd == 'wednesday' : d = 2
		if nthd == 'thursday' : d = 3
		if nthd == 'friday' : d = 4
		if nthd == 'saturday' : d = 5
		if nthd == 'sunday' : d = 6
		m = dt.month
		y = dt.year
		ld = 31
		if g == 1 :
			while oo < ee :
				if m > 12 :
					m = m % 12
					y = y + 1
				ld = max(week[d] for week in calendar.monthcalendar(y, m))
				dt = dt.replace(y,m,ld)
				oo = datetime.toordinal(dt)
				if oo > nn :
					pile.append([prepret(dt.year,dt.month,dt.day),title,amt])
				m = m + 1
		else :
			while oo < ee :
				if m > 12 :
					m = m % 12
					y = y + 1
				ld = 31
				for week in calendar.monthcalendar(y, m) :
					if week[d] != 0 : ld = min(ld, week[d])
				dt = dt.replace(y,m,ld)
				oo = datetime.toordinal(dt)
				if oo > nn :
					pile.append([prepret(dt.year,dt.month,dt.day),title,amt])
				m = m + 1
				
	if calctype == 'lastdayofnthmonth' :
		n = datetime.now()
		nn = datetime.toordinal(n)
		m = int(nth)
		y = n.year
		d = calendar.monthrange(y,m)[1]
		dt = datetime.now()
		dt = dt.replace(y,m,d)
		oo = datetime.toordinal(dt)
		c = 1
		while oo < ee :
			if m > 12 :
				m = m % 12
				y = y + 1
			ld = calendar.monthrange(y,m)[1]	
			dt = dt.replace(y,m,ld)
			oo = datetime.toordinal(dt)
			if oo > nn :
				pile.append([prepret(dt.year,dt.month,dt.day),title,amt])
			m = m + int(nth)
								
	if calctype == 'annually' :
		n = datetime.now()
		nn = datetime.toordinal(n)
		dt = datetime.strptime(startdate,'%y%m%d')
		m = dt.month
		d = dt.day
		y = dt.year
		oo = datetime.toordinal(dt)
		while oo < nn :
			y = y + 1
			dt = dt.replace(y,m,d)
			oo = datetime.toordinal(dt)

		if nn < oo :
			pile.append([prepret(dt.year,dt.month,dt.day),title,amt])


	if calctype == 'once' :
		n = datetime.now()
		nn = datetime.toordinal(n)
		dt = datetime.strptime(startdate,'%y%m%d')
		m = dt.month
		d = dt.day
		y = dt.year
		oo = datetime.toordinal(dt)
		if oo > nn :
			pile.append([prepret(dt.year,dt.month,dt.day),title,amt])
			
	if calctype == 'pre' :
		n = datetime.now()
		pile.append([prepret(n.year,n.month,n.day),title,amt])	
			
	return(pile)
	
f = open( cdr +'/items.txt','r')
d = []
for l in f :
	if l.strip() != '' :
		d.append(l.split(';'))
f.close()

dlen = 0
out = []
sds = []
enddate = '180101'

for t in d :
	dlen = max(dlen,len(t[0]))
	s = getnth(t[0], t[1], t[2], t[3], t[4], enddate)
	for i in s: out.append(i)

out.sort(key=lambda x: x[0])

bal = 0
olen = 0
nulen = 0
dtlen = 12
po = []
minbal = 9999999
maxbal = -9999999
for o in out :
	nu = o[2].strip()
	nulen = max(len(nu), nulen)
	bal = bal + int(nu)
	minbal = min(minbal,bal)
	maxbal = max(maxbal,bal)

print('minbal = ' + str(minbal))
print('maxbal = ' + str(maxbal))
	
sep = (padstr('|-','-',dtlen) + '-+-' + padstr('','-',dlen) + '-+-' + padstr('','-',7) + '-+-' + padstr('','-',7) + '-+-'  + padstr('','-',7) + '-+-'  + padstr('','-',7) + '-|')

print(sep)

hed = (padstr('| DATE',' ',dtlen) + ' | ' + padstr('TRANSACTION',' ',dlen) + ' | ' + padstr('AMOUNT',' ',7) + ' | '  + padstr('BALANCE',' ',7) + ' | ' + padstr('',' ',7) + ' | ' + padstr('',' ',7) + ' |')

print(hed)
print(sep)

rtt = 0
m = 0
om = int(out[0][0][1].split('-')[1])
mbal = 0
for o in out :
	nu = o[2].strip()
	nga = 0
	psa = 0
	nbr = '       '
	pbr = '       '
	rtt = rtt + int(nu)
	if rtt < 0 :
		nga = int(7.0 * float(abs(rtt))/abs(minbal))
		nbr = prepadstr('',"=",nga)
		nbr = prepadstr(nbr," ",7)
	if rtt > 0 :
		psa = int(7.0 * (float(abs(rtt))/float(max(maxbal,0))))
		pbr = prepadstr('',"=",psa)
		pbr = padstr(pbr," ",7)
	ol = ('| ' + o[0][1] + ' | ' + padstr(o[1],'.',dlen) + ' | ' + padstr(nu,' ',7) + ' | ' + padstr(str(rtt),' ',7)  + ' | ' + nbr  + ' | ' + pbr + ' |')
	olen = max(len(ol), olen)
	
	m = int(o[0][1].split('-')[1])
	if m != om :
		msu = ('| ' + '          ' + ' | ' + padstr('',' ',dlen) + ' | ' + padstr(str(mbal),' ',7) + ' | ' + padstr('',' ',7)  + ' | ' + '       '  + ' | ' + '       ' + ' |')
		print(sep)		
		print(msu)
		print(sep)		
		mbal = int(nu)
		om = m
		print(ol + ' ')
	else :	
		mbal = mbal + int(nu)
		print(ol + ' ')

print(sep)

