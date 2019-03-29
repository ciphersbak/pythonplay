import hashlib
import math
import struct
import re

# stmt_lower = "select 'Slavik' from dual"
# stmt_lower = "UPDATE PS_PROJ_RESOURCE SET PC_DISTRIB_STATUS = 'L', PROCESS_INSTANCE = 3771317 WHERE ( CST_DISTRIB_STATUS = 'N' AND BI_DISTRIB_STATUS IN ('N', 'U') AND REV_DISTRIB_STATUS = 'N') AND SYSTEM_SOURCE NOT IN ('PRC', 'PRP', 'PRR') AND BUSINESS_UNIT = 'CERN' AND TRANS_DT BETWEEN TO_DATE('2015-11-01', 'YYYY-MM-DD') AND TO_DATE('2017-04-29', 'YYYY-MM-DD') AND PC_DISTRIB_STATUS <> 'L'"
# stmt_lower = "UPDATE PS_PRT_PRICE3 SET PC_TEMPLATE_ID = ' ', TEMPLATE_TYPE = ' ' , RATE_DEF_TYPE = ' ' WHERE PROCESS_INSTANCE = 3771317 AND PC_TEMPLATE_ID <> ' ' AND TEMPLATE_TYPE <> ' ' AND RATE_DEF_TYPE <> ' '"
# stmt_lower = "UPDATE PS_BI_LINE_TAX_DTL SET CURRENCY_CD_XEU = 'EUR', TAX_AMT_BSE = ROUND(((((TAX_AMT) / (1))) * (1)), 3), TAX_AMT_XEU = ROUND(((((TAX_AMT) / (1))) * (1)), 3) WHERE INVOICE IN ( SELECT T1.INVOICE FROM PS_BI_CURCNV_TAO3 T1 , PS_BI_LINE LN WHERE T1.PROCESS_INSTANCE = 3771362 AND T1.BUSINESS_UNIT = PS_BI_LINE_TAX_DTL.BUSINESS_UNIT AND T1.BUSINESS_UNIT = LN.BUSINESS_UNIT AND T1.INVOICE = PS_BI_LINE_TAX_DTL.INVOICE AND T1.INVOICE = LN.INVOICE AND PS_BI_LINE_TAX_DTL.LINE_SEQ_NUM = LN.LINE_SEQ_NUM AND T1.RATE_MULT = 1 AND T1.RATE_DIV = 1 AND T1.RATE_MULT_XEU = 1 AND T1.RATE_DIV_XEU = 1 AND T1.RATE_MULT_IU = 0 AND T1.RATE_DIV_IU = 1 AND T1.BI_CURRENCY_CD = 'EUR' AND T1.BASE_CURRENCY = 'EUR' AND T1.CURRENCY_CD_XEU = 'EUR' AND T1.BUSINESS_UNIT_TO = ' ' AND T1.PROCESS_FLG = 'A' AND (T1.BI_BU_TAX_IND <> '1' OR (T1.INVOICE_TYPE = 'ACR' OR LN.ADJ_LINE_TYPE = 'ACR'))) AND BUSINESS_UNIT LIKE '%'"
stmt_lower = "UPDATE PS_PROJ_RESOURCE SET PC_DISTRIB_STATUS = 'L', PROCESS_INSTANCE = 3771317 WHERE ( CST_DISTRIB_STATUS = 'N' AND BI_DISTRIB_STATUS IN ('N', 'U') AND REV_DISTRIB_STATUS = 'N') AND SYSTEM_SOURCE NOT IN ('PRC', 'PRP', 'PRR') AND BUSINESS_UNIT = 'CERN' AND TRANS_DT BETWEEN TO_DATE('2015-11-01','YYYY-MM-DD') AND TO_DATE('2017-04-29','YYYY-MM-DD') AND PC_DISTRIB_STATUS <> 'L'"
# stmt_lower = "DELETE FROM PS_PRT_PRICEX3 WHERE PROCESS_INSTANCE = 3771319 AND (PROCESS_INSTANCE, BUSINESS_UNIT, PROJECT_ID, ACTIVITY_ID, RESOURCE_ID) IN ( SELECT 3771319 , PRT.BUSINESS_UNIT , PRT.PROJECT_ID , PRT.ACTIVITY_ID , PRT.RESOURCE_ID FROM PS_PRT_PRICE3 PRT WHERE PRT.PROCESS_INSTANCE = 3771319)"
stmt_upper = "SELECT 'Slavik' FROM DUAL"

hashvalue = struct.unpack('IIII', hashlib.md5(stmt_lower + '\x00').digest())[3]
# print 'hashvalue : ' + str(hashvalue)
h = ''
for i in struct.unpack('IIII', hashlib.md5(stmt_lower + '\x00').digest()):
	h += hex(i)[2:]
# print 'hexvalue: ' + str(h)

def sqlid_2_hash(sqlid):
	sum = 0
	i = 1
	# the string below is the key, note it is missing some letters intentionally
	alphabet = '0123456789abcdfghjkmnpqrstuvwxyz'
	for ch in sqlid:
		sum += alphabet.index(ch) * (32**(len(sqlid) - i))
		i += 1
	return sum % (2 ** 32)
  
def stmt_2_sqlid(stmt_lower):
	arr_stmt = stmt_lower.split("'")
	int_indx = 0
	stmt_lower = ''
	for str_stmt in arr_stmt:
		print str(int_indx) + " --> Before statement: " + str_stmt
		if int_indx%2 == 0:
			str_stmt = re.sub(r'\s+', ' ', str_stmt) + "'"

		else:
			str_stmt += "'"
		stmt_lower += str_stmt
		print str(int_indx) + " --> After statement: " + str_stmt
		int_indx += 1
	print stmt_lower[:-1]
	stmt_lower = stmt_lower[:-1]
	h = hashlib.md5(stmt_lower.lstrip().rstrip() + '\x00').digest()
	(d1,d2,msb,lsb) = struct.unpack('IIII', h)
	sqln = msb * (2 ** 32) + lsb	
	stop = int(math.log(sqln, math.e) / math.log(32, math.e) + 1)
	print 'stop : ' + str(stop)
	# print 'sqln : ' + str(sqln) + " : " + str(msb) + " : " + str(lsb)
	sqlid = ''
	# the string below is the key, note it is missing some letters intentionally
	alphabet = '0123456789abcdfghjkmnpqrstuvwxyz'
	for i in range(0, stop):
		sqlid = alphabet[(sqln / (32 ** i)) % 32] + sqlid		
	return sqlid 
  
def stmt_2_hash(stmt_lower):
  return struct.unpack('IIII', hashlib.md5(stmt_lower.lstrip().rstrip() + '\x00').digest())[3]

print 'Hash Value : ' + str(stmt_2_hash(stmt_lower))
print 'SQLID: ' + str(stmt_2_sqlid(stmt_lower))
