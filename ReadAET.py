
#with open("D:\PP_Oracle\\1_Work\\FSCM\\Bugs\\PC_POADJUST\\AE_PC_POADJUST_2056943_0720100856.AET", "r") as f:
#    for line in f:
#		boolSql = False
#		if line[:2] == "--":
#			line = line.rstrip('\n')
#			if line.endswith("(SQL)"):
#				boolSql = True
#				print line
#			if line.startswith("-- Row(s) affected:"):
#				print line
#		if boolSql:
#			line = f.readline()
#			print line
import os
import cx_Oracle
import datetime

def main():
	# Create Connection
	db = cx_Oracle.connect('SYSADM', 'SYSADM', '192.168.56.101:1522/EP92U021')
	# Create Cursor
	cur = db.cursor()
	# Read AET File
	f = open("D:\PP_Oracle\\1_Work\\FSCM\\Bugs\\PC_POADJUST\\AE_PC_POADJUST_2056943_0720100856.AET",'r')
	# Read First Line
	line = f.readline()
	# Get Base File Name
	strArrFileName = os.path.basename(f.name).split("_")
	# Get Process Instance from File Name
	intPrcsInstance = strArrFileName[len(strArrFileName) -2]
	rows = []
	intSeqNbr = 1
	# Loop
	while line:
		boolSql = False
		if line[:2] == "--":
			line = line.rstrip('\n')
			if line.endswith("(SQL)"):
				boolSql = True
				strArrAITRP = line.split(" ")
				#print strArrAITRP[1] + " >> " + strArrAITRP[2].strip(".").strip("(").strip(")")
				strAITRPLine = strArrAITRP[1] + " >> " + strArrAITRP[2].strip(".").strip("(").strip(")") + " >> " + str(intPrcsInstance)
				strSQLType = " "
				tSTARTTIME = strArrAITRP[1]
			if line.startswith("-- Row(s) affected:"):
				strArrAITRP = line.split(" ")
				#print strArrAITRP[3]
				strAITRPLine = strAITRPLine + " >> " + strArrAITRP[3]
				print strAITRPLine
				strAEAPPLID = strAITRPLine.split(" >> ")[1].split(".")[0]
				strSQLID = strAITRPLine.split(" >> ")[1].replace(strAEAPPLID, "")[1:]
				tENDTIME = datetime.datetime.now().time()
				tCALCTIME = datetime.datetime.now().time()
				row = (intPrcsInstance, intSeqNbr, strAEAPPLID, strSQLID, strSQLType, 0, strArrAITRP[3], str(tSTARTTIME), str(tENDTIME), str(tCALCTIME), ' ')
				rows.append(row)
				#InsertIntoDB(cur, rows)
				intSeqNbr += 1
			# elif not line.endswith("(SQL)") and "(" in :
				# print line
				# strArrAITRP = line.split(" ")
				# #print strArrAITRP[1] + " >> " + strArrAITRP[2].strip(".").strip("(").strip(")")
				# strAITRPLine = strArrAITRP[1] + " >> " + strArrAITRP[2].strip(".").strip("(").strip(")") + " >> " + str(intPrcsInstance)
				# strSQLType = " "
				# tSTARTTIME = strArrAITRP[1]
				
				# strAEAPPLID = strAITRPLine.split(" >> ")[1].split(".")[0]
				# strSQLID = strAITRPLine.split(" >> ")[1].replace(strAEAPPLID, "")[1:]
				# tENDTIME = datetime.datetime.now().time()
				# tCALCTIME = datetime.datetime.now().time()
				# row = (intPrcsInstance, intSeqNbr, strAEAPPLID, strSQLID, strSQLType, 0, 0, str(tSTARTTIME), str(tENDTIME), str(tCALCTIME), ' ')
				# rows.append(row)
				# #InsertIntoDB(cur, rows)
				# intSeqNbr += 1
				
		if boolSql:
			line = f.readline()
			if line.startswith("INSERT"):
				#print "INSERT"
				strAITRPLine = strAITRPLine + " >> " + "INSERT"
				strSQLType = "INSERT"
			if line.startswith("UPDATE"):
				#print "UPDATE"
				strAITRPLine = strAITRPLine + " >> " + "UPDATE"
				strSQLType = "UPDATE"
			if line.startswith("DELETE"):
				#print "DELETE"
				strAITRPLine = strAITRPLine + " >> " + "DELETE"
				strSQLType = "DELETE"
			if line.startswith("SELECT"):
				#print "SELECT"
				strAITRPLine = strAITRPLine + " >> " + "SELECT"
				strSQLType = "SELECT"
			if line.startswith("RUN RECSTATS"):
				#print "STATS"
				strAITRPLine = strAITRPLine + " >> " + "STATS"
				strSQLType = "STATS"
			if line[1:].startswith("Select"):
				#print "SELECT"	
				strAITRPLine = strAITRPLine + " >> " + "SELECT"	
				strSQLType = "SELECT"
		line = f.readline()
	f.close()
	InsertIntoDB(cur, rows)
	db.commit()
	
def InsertIntoDB(cur, rows):
	# print str(row)
    #Insert into SQL Table
	#cur.executemany("INSERT INTO PSPPPARSEAET (PROCESS_INSTANCE, SEQ_NBR, AE_APPLID, SQLID, PM_SQL_TYPE, COUNTER, SQLROWS_2, START_TIME, END_TIME, CALC_TIME, SQLTEXT2) values (:1, :2, :3, :4, :5, :6, :7, TO_TIMESTAMP(:8, 'HH24:MI:SS.FF'), TO_TIMESTAMP(:9, 'HH24:MI:SS.FF'), TO_TIMESTAMP(:10, 'HH24:MI:SS.FF'), :11)", [row])
	cur.executemany("INSERT INTO PSPPPARSEAET (PROCESS_INSTANCE, SEQ_NBR, AE_APPLID, SQLID, PM_SQL_TYPE, COUNTER, SQLROWS_2, START_TIME, END_TIME, CALC_TIME, SQLTEXT2) values (:1, :2, :3, :4, :5, :6, :7, TO_TIMESTAMP(:8, 'HH24:MI:SS.FF'), TO_TIMESTAMP(:9, 'HH24:MI:SS.FF'), TO_TIMESTAMP(:10, 'HH24:MI:SS.FF'), :11)", rows)
	
if __name__ == "__main__"	:
	main()