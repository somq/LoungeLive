#! /usr/bin/env python
import datetime as DT
import json
import pytz
from dateutil import parser
from dateutil import tz

def dateNow():
	import time, json
	from datetime import datetime as dt
	your_date = dt.now()
	data = json.dumps(time.mktime(your_date.timetuple())*1000)
	return data # data send to javascript

def findPunctuationType(stringToFindIn):
    puncArray = ['.', ',', ':', ';', ' ' ]
    for i in puncArray:
        if i in stringToFindIn:
            return i
        
        
def formatDate(feedDate, feedHour, timeZone):

	tz_str = '''	-12 Y
	-11 X NUT SST
	-10 W CKT HAST HST TAHT TKT
	-9 V AKST GAMT GIT HADT HNY
	-8 U AKDT CIST HAY HNP PST PT
	-7 T HAP HNR MST PDT
	-6 S CST EAST GALT HAR HNC MDT
	-5 R CDT COT EASST ECT EST ET HAC HNE PET
	-4 Q AST BOT CLT COST EDT FKT GYT HAE HNA PYT
	-3 P ADT ART BRT CLST FKST GFT HAA PMST PYST SRT UYT WGT
	-2 O BRST FNT PMDT UYST WGST
	-1 N AZOT CVT EGT
	0 Z EGST GMT UTC WET WT
	1 A CET DFT WAT WEDT WEST
	2 B CAT CEDT CEST EET SAST WAST
	3 C EAT EEDT EEST IDT MSK
	4 D AMT AZT GET GST KUYT MSD MUT RET SAMT SCT
	5 E AMST AQTT AZST HMT MAWT MVT PKT TFT TJT TMT UZT YEKT
	6 F ALMT BIOT BTT IOT KGT NOVT OMST YEKST
	7 G CXT DAVT HOVT ICT KRAT NOVST OMSST THA WIB
	8 H ACT AWST BDT BNT CAST HKT IRKT KRAST MYT PHT SGT ULAT WITA WST
	9 I AWDT IRKST JST KST PWT TLT WDT WIT YAKT
	10 K AEST ChST PGT VLAT YAKST YAPT
	11 L AEDT LHDT MAGT NCT PONT SBT VLAST VUT
	12 M ANAST ANAT FJT GILT MAGST MHT NZST PETST PETT TVT WFT
	13 FJST NZDT
	11.5 NFT
	10.5 ACDT LHST
	9.5 ACST
	6.5 CCT MMT
	5.75 NPT
	5.5 SLT
	4.5 AFT IRDT
	3.5 IRST
	-2.5 HAT NDT
	-3.5 HNT NST NT
	-4.5 HLV VET
	-9.5 MART MIT'''

	tzd = {}
		
    #format initial date string eg. fools typing 12.30 instead of 12:30
	try:
		datePuncType = findPunctuationType(feedHour)
		hourPuncType = findPunctuationType(feedHour)
		feedDate = feedDate.replace(datePuncType, '-')
		feedHour = feedHour.replace(datePuncType, ':')
		
		dateString = feedDate + ' ' + feedHour + ' ' + timeZone 
	except:
		dateString = 'undefined'

	if dateString != 'undefined':
		for tz_descr in map(str.split, tz_str.split('\n')):
			tz_offset = int(float(tz_descr[0]) * 3600)
			for tz_code in tz_descr[1:]:
				tzd[tz_code] = tz_offset
		dateParsed = parser.parse(dateString, tzinfos=tzd, fuzzy=True, dayfirst=True)

		dthandler = lambda obj: (
			obj.isoformat()
			if isinstance(obj, DT.datetime)
			or isinstance(obj, DT.date)
			else None)
		dateJson = json.dumps(dateParsed, default=dthandler)
		return dateJson
	else:
		print 'error parsing date'
		pass
		# dateJson = json.dumps("1900-01-01T00:00:00+01:00")
		# return dateJson
