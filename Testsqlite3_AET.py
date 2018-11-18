import os
import datetime
# Establish DB connection
import cx_Oracle
# Read multiple files from a directory
from itertools import islice
from os import listdir
from os.path import isfile, join, dirname, basename, realpath
# This is what makes it run in parallel
from multiprocessing import Process
import sqlite3

# Create Connection
db_con = sqlite3.connect('example.db')
# Create Cursor
cur = db_con.cursor()
# Test Global vs Loal Variables
bool_negative_row_delete = False
int_iteration = 0
str_current_ae_sqlid_name = ""
str_arr_parent_ae_sqlid_name = ["Root"]

def get_prcs_inst(str_file_name):
    """Get the process instance from the file name"""
    str_arr_file_names = str_file_name.split("_")
    return str_arr_file_names[len(str_arr_file_names) - 2]

def read_sql(str_cur_line, itr_set_lines):
    """Read select statement from AET file"""
    str_sql_stmt = ""
    while True:
        # Strip new line character and check
        str_cur_line = str_cur_line.rstrip('\n')
        if str_cur_line.startswith("/"):
            break
        str_sql_stmt += str_cur_line
        str_cur_line = str(next(itr_set_lines))
    # str_sql_stmt = sqlparse.format(str_sql_stmt,
    #                                       reindent=True,
    #                                       keyword_case='upper')
    # print "SQL stmt: " + str_sql_stmt
    return str_sql_stmt

def prcs_call_section(str_cur_line, itr_set_lines, dict_AET_prcs_dtls, int_ln_indx, str_action_name, insert_rows):
    """Process call section actions"""
    str_arr_cur_line = str_cur_line.split(" ")
    str_timestamp = str_arr_cur_line[1]
    str_sql_id = str_arr_cur_line[2][1:].strip(".").strip("(").strip(")")
    str_ae_appl_id = str_sql_id.split(".")[0]
    str_ae_section_name = str_sql_id.split(".")[1]
    str_ae_step_name = str_sql_id.split(".")[2]

def prcs_log_message(str_cur_line, itr_set_lines, dict_AET_prcs_dtls, int_ln_indx, str_action_name, insert_rows):
    """Process log message actions"""
    str_arr_cur_line = str_cur_line.split(" ")
    str_timestamp = str_arr_cur_line[1]
    str_sql_id = str_arr_cur_line[2][1:].strip(".").strip("(").strip(")")
    str_ae_appl_id = str_sql_id.split(".")[0]
    str_ae_section_name = str_sql_id.split(".")[1]
    str_ae_step_name = str_sql_id.split(".")[2]

def actn_not_found(str_cur_line, itr_set_lines, dict_AET_prcs_dtls, int_ln_indx, str_action_name, insert_rows):
    """When action is not found"""
    str_action_name = get_action(str_cur_line)
    if str_action_name.startswith("Call Section"):
        prcs_call_section(str_cur_line, itr_set_lines, dict_AET_prcs_dtls, int_ln_indx, str_action_name, insert_rows)
    else:
        # This is needed to capture any additional comments, e.g., Temp Table Instance is locked by another run of the AE 
        print "  No action found for line: " + str_cur_line


def check_if_valid_stmt(str_cur_line):
    """Check for the second field and if is a valid time stamp"""
    """Tools changed the time format - Works with 8.55/56, notice the time separator, it is a semi-colon"""
    str_timeformat = "%H:%M:%S.%f"
    """For 8.52.xx, notice the time separator, it is a dot"""
    # str_timeformat = "%H.%M.%S"
    str_arr_cur_line = str_cur_line.split(" ")
    if len(str_arr_cur_line) >= 2:
        str_timestamp = str_cur_line.split(" ")[1]
        # print "Time stamp: " + str_timestamp
    try:
        validtime = datetime.datetime.strptime(str_timestamp, str_timeformat)
    except Exception as e:
        return False
    return True

def get_action(str_cur_line):
    """Get the action name from the provided line"""
    str_arr_cur_line = str_cur_line.split("(")
    str_action_name = ""
    if len(str_arr_cur_line) > 1:
        str_action_name = str_arr_cur_line[len(str_arr_cur_line) - 1].replace(")", "")
    return str_action_name

def read_command(str_cur_line, itr_set_lines, dict_AE_dtls):
    """Read -- from AET file as command"""
    # Capture COMMIT, Restarts Data Check Points, BIND Variables, Buffers
    bool_bind_var_found = False
    bool_buffer_found = False
    global bool_negative_row_delete, int_iteration
    int_cur_ln_indx = 0
    int_cur_cmd_indx = 0

    while True:
        str_cur_line = str_cur_line.rstrip('\n')
        int_cur_ln_indx += 1
        if len(str_cur_line) == 0:
            break
        if not str_cur_line.startswith("/"):
            # print "Command: " + str_cur_line
            if str_cur_line.startswith("Restart Data CheckPointed"):
                # dict_AE_dtls["restart_data_checkpointed"] = True
                dict_AE_dtls["restart_data_checkpointed"] = "CKPOINT"
                bool_buffer_found = False
                bool_bind_var_found = False
            elif str_cur_line.startswith("COMMIT"):
                # dict_AE_dtls["commit"] = True
                dict_AE_dtls["commit"] = "COMMIT"
                bool_buffer_found = False
                bool_bind_var_found = False
            elif str_cur_line[3:].startswith("Row(s) affected"):
                dict_AE_dtls["rows_affected"] = str_cur_line.split(":")[1].strip(" ")
                # DELETE statements have been known to set 'Row(s) affected' to '-1' on certain platforms
                if int(dict_AE_dtls["rows_affected"]) < 0:
                    bool_negative_row_delete = True
                bool_buffer_found = False
                bool_bind_var_found = False
            elif str_cur_line[3:].startswith("Buffers"):
                bool_buffer_found = True
                bool_bind_var_found = False
                dict_AE_dtls["buffers"] = []
                int_cur_cmd_indx = int_cur_ln_indx
            elif str_cur_line[3:].startswith("Bind variables"):
                bool_bind_var_found = True
                bool_buffer_found = False
                dict_AE_dtls["bindVariables"] = []
                int_cur_cmd_indx = int_cur_ln_indx
            elif check_if_valid_stmt(str_cur_line):
                if "Application Engine" not in str_cur_line:
                    str_arr_cur_line = str_cur_line.split("Iteration")
                    if len(str_arr_cur_line) > 1:
                        dict_AE_dtls["Iteration"] = str_cur_line.split("Iteration")[1].strip(" ").split(" ")[0].strip(" ")
                        int_iteration = str_cur_line.split("Iteration")[1].strip(" ").split(" ")[0].strip(" ")
            if bool_buffer_found:
                if int_cur_cmd_indx != int_cur_ln_indx and not check_if_valid_stmt(str_cur_line):
                    # print "str_cur_line: " + str_cur_line + " length: " + str(len(str_cur_line))
                    dict_AE_dtls["buffers"].append(str_cur_line[4:].split(")")[1].strip(" "))
                    # pass

            if bool_bind_var_found:
                if int_cur_cmd_indx != int_cur_ln_indx:
                    dict_AE_dtls["bindVariables"].append(str_cur_line[4:].split(")")[1].strip(" "))

        str_cur_line = str(next(itr_set_lines))

def prcs_sql(str_cur_line, itr_set_lines, dict_AET_prcs_dtls, int_ln_indx, str_action_name, insert_rows):
    """Process SQL actions"""
    global int_iteration
    global str_arr_parent_ae_sqlid_name
    str_arr_cur_line = str_cur_line.split(" ")
    str_timestamp = str_arr_cur_line[1]
    str_sql_id = str_arr_cur_line[2][1:].strip(".").strip("(").strip(")")
    str_ae_appl_id = str_sql_id.split(".")[0]
    str_ae_section_name = str_sql_id.split(".")[1]
    str_ae_step_name = str_sql_id.split(".")[2]

    str_sql_stmt = " "
    dict_AE_dtls = {}
    dict_AE_dtls["restart_data_checkpointed"] = " "
    dict_AE_dtls["commit"] = " "
    dict_AE_dtls["rows_affected"] = 0
    dict_AE_dtls["Iteration"] = 0
    dict_AE_dtls["sql_type"] = " "
    dict_AE_dtls["buffers"] = []
    dict_AE_dtls["bindVariables"] = []
    
    str_cur_line = str(next(itr_set_lines))
    while True:
        str_cur_line = str_cur_line.rstrip('\n')
        if len(str_cur_line) == 0:
            break
        # print "Current line: " + str_cur_line
        # Identify DML/DDL commands
        if str_cur_line.upper().startswith("INSERT"):
            dict_AE_dtls["sql_type"] = "Insert"
            str_sql_stmt = read_sql(str_cur_line, itr_set_lines)
        elif str_cur_line.upper().startswith("UPDATE"):
            dict_AE_dtls["sql_type"] = "Update"
            str_sql_stmt = read_sql(str_cur_line, itr_set_lines)
        elif str_cur_line.upper().startswith("DELETE"):
            dict_AE_dtls["sql_type"] = "Delete"
            str_sql_stmt = read_sql(str_cur_line, itr_set_lines)
        elif str_cur_line.upper().startswith("TRUNCATE"):
            dict_AE_dtls["sql_type"] = "Truncate"
            str_sql_stmt = read_sql(str_cur_line, itr_set_lines)    
        elif str_cur_line.upper().startswith("SELECT"):
            dict_AE_dtls["sql_type"] = "Select"
            str_sql_stmt = read_sql(str_cur_line, itr_set_lines)
            # RUN RECSTATS or RECSTATS
        elif "RECSTATS" in str_cur_line.upper():
            dict_AE_dtls["sql_type"] = "Stats"
            str_sql_stmt = read_sql(str_cur_line, itr_set_lines)
            # This is %Select or %SelectInit
        elif str_cur_line[1:].upper().startswith("SELECT"):
            dict_AE_dtls["sql_type"] = "Select"
            str_sql_stmt = read_sql(str_cur_line, itr_set_lines)
            # Identify COMMIT, Buffers, Bind Variables and Restart Checkpoints
        elif str_cur_line[:2] == "--":
            str_sql_type = "Command"
            itr_set_lines = read_command(str_cur_line, itr_set_lines, dict_AE_dtls)
            break
        str_cur_line = str(next(itr_set_lines))

    dict_AE_dtls["parent"] = str_arr_parent_ae_sqlid_name[len(str_arr_parent_ae_sqlid_name) - 2]
    if str_action_name == 'Do Fetch':
        str_action_name = "Do Select"
    dict_AE_dtls["action"] = str_action_name
    dict_AE_dtls["seq_nbr"] = int_ln_indx
    dict_AE_dtls["process"] = str_ae_appl_id
    dict_AE_dtls["section"] = str_ae_section_name
    dict_AE_dtls["step"] = str_ae_step_name
    dict_AE_dtls["sql_id"] = str_sql_id
    dict_AE_dtls["start_time"]= str_timestamp
    dict_AE_dtls["end_time"]= " "
    dict_AE_dtls["calc_time"]= " "
    dict_AE_dtls["sql_statement"] = str_sql_stmt
    dict_AE_dtls["ae_run_data"] = str(str_arr_parent_ae_sqlid_name).replace(",", " --> ") + " --> " + str_action_name
        
    # dict_AET_prcs_dtls["dtls"].append(dict_AE_dtls)
    insert_row = (int(dict_AET_prcs_dtls["Instance"]),
                  int_ln_indx,
                  dict_AE_dtls["parent"],
                  dict_AE_dtls["process"],
                  dict_AE_dtls["section"]+"."+dict_AE_dtls["step"],
                  dict_AE_dtls["action"],
                  dict_AE_dtls["sql_type"],
                  dict_AE_dtls["Iteration"],
                  # This is COUNTER
                  int(int_iteration),
                  int(dict_AE_dtls["rows_affected"]),
                  # Store CHKPOINT and COMMIT
                  str(dict_AE_dtls["restart_data_checkpointed"]),
                  str(dict_AE_dtls["commit"]),
                  dict_AE_dtls["start_time"],
                  dict_AE_dtls["start_time"],
                  dict_AE_dtls["start_time"],
                  # Store Buffers and Bind Variables
                  str(dict_AE_dtls["buffers"]),
                  str(dict_AE_dtls["bindVariables"]),
                  dict_AE_dtls["sql_statement"],
                  dict_AE_dtls["ae_run_data"]
                  )
    # print json.dumps(dict_AE_dtls, sort_keys=False, indent=2)
    # print "insert_row " + str(insert_row)
    # insert_rows.append(insert_row)
    insert_into_db(cur, insert_row)

def prcs_peoplecode(str_cur_line, itr_set_lines, dict_AET_prcs_dtls, int_ln_indx, str_action_name, insert_rows):
    """Process PeopleCode actions"""

    global int_iteration
    global str_arr_parent_ae_sqlid_name

    str_arr_cur_line = str_cur_line.split(" ")
    str_timestamp = str_arr_cur_line[1]
    str_pc_id = str_arr_cur_line[2][1:].strip(".").strip("(").strip(")")
    str_ae_appl_id = str_pc_id.split(".")[0]
    str_ae_section_name = str_pc_id.split(".")[1]
    str_ae_step_name = str_pc_id.split(".")[2]
    str_ae_action_name = str_action_name

    dict_AE_dtls = {}
    dict_AE_dtls["restart_data_checkpointed"] = " "
    dict_AE_dtls["commit"] = " "
    dict_AE_dtls["buffers"] = []
    dict_AE_dtls["bindVariables"] = []

    # print "PeopleCode: " + str_cur_line
    dict_AE_dtls["seq_nbr"] = int_ln_indx
    dict_AE_dtls["parent"] = str_arr_parent_ae_sqlid_name[len(str_arr_parent_ae_sqlid_name) - 2]
    dict_AE_dtls["action"] = str_action_name
    dict_AE_dtls["sql_type"] = "PeopleCode"
    dict_AE_dtls["process"] = str_ae_appl_id
    dict_AE_dtls["section"] = str_ae_section_name
    dict_AE_dtls["step"] = str_ae_step_name
    dict_AE_dtls["sql_id"] = str_pc_id
    # dict_AE_dtls["action"] = str_ae_action_name
    dict_AE_dtls["start_time"]= str_timestamp
    dict_AE_dtls["end_time"]= " "
    dict_AE_dtls["calc_time"]= " "
    dict_AE_dtls["sql_statement"] = " "
    dict_AE_dtls["rows_affected"] = 0
    dict_AE_dtls["ae_run_data"] = str(str_arr_parent_ae_sqlid_name).replace(",", " --> ") + " --> " + str_action_name
    # dict_AET_prcs_dtls["dtls"].append(dict_AE_dtls)

    insert_row = (int(dict_AET_prcs_dtls["Instance"]),
                  int_ln_indx,
                  dict_AE_dtls["parent"],
                  dict_AE_dtls["process"],
                  dict_AE_dtls["section"]+"."+dict_AE_dtls["step"],
                  dict_AE_dtls["action"],
                  dict_AE_dtls["sql_type"],
                  0,
                  int(int_iteration),
                  int(dict_AE_dtls["rows_affected"]),
                  # Store CHKPOINT and COMMIT
                  str(dict_AE_dtls["restart_data_checkpointed"]),
                  str(dict_AE_dtls["commit"]),
                  dict_AE_dtls["start_time"],
                  dict_AE_dtls["start_time"],
                  dict_AE_dtls["start_time"],
                  # Store Buffers and Bind Variables
                  str(dict_AE_dtls["buffers"]),
                  str(dict_AE_dtls["bindVariables"]),
                  dict_AE_dtls["sql_statement"],
                  dict_AE_dtls["ae_run_data"]
                  )

    # print json.dumps(dict_AE_dtls, sort_keys=False, indent=2)
    # insert_rows.append(insert_row)
    insert_into_db(cur, insert_row)

def processAETSet(int_prcs_inst, lst_set_lines, int_ln_indx):
    # Create Connection. This is my local DB
    # db_con = cx_Oracle.connect("QAEADMIN/QAEADMIN@T56PPTLS.oradev.oraclecorp.com")
    # Create Cursor
    # cur = db_con.cursor()
    print "Total rows in the set: " + str(len(lst_set_lines))
    dict_AET_prcs_dtls = {}
    str_file_name = "test"
    dict_AET_prcs_dtls["Summary"] = "This is autogenerated using ReadPSAET python program"
    dict_AET_prcs_dtls["Instance"] = int_prcs_inst
    dict_AET_prcs_dtls["Name"] = basename(str_file_name).split(int_prcs_inst)[0][3:].strip("_")

    # Define Dictionary. Add actions here that you want to capture
    dict_AET_prcs_dtls["dtls"] = []
    lst_avlbl_actns = { "SQL" : prcs_sql,
                       "PeopleCode" : prcs_peoplecode,
                       "Do Select" : prcs_sql,
                       "Do When" : prcs_sql,
                       "Do While" : prcs_sql,
                       "Do Until" : prcs_sql,
                       "Do Fetch" : prcs_sql,
                       "Call Section" : prcs_call_section,
                       "Log Message" : prcs_log_message
                     }

    # int_ln_indx = 0
    int_total_ln_indx = 0
    insert_rows = []

    itr_set_lines = iter(lst_set_lines)

    for str_cur_line in itr_set_lines:
        # str_cur_line = str(str_cur_line)
        str_cur_line = str(str_cur_line).rstrip('\n')
        int_total_ln_indx += 1
        # print "Line: " + str_cur_line
        # print "Length: " + str(len(str_cur_line))
        if str_cur_line[:2] == "--":
            if check_if_valid_stmt(str_cur_line):
                # print "Line: " + str_cur_line
                str_action_name = get_action(str_cur_line)
                if len(str_action_name) > 0:
                    int_ln_indx += 1
                    # print "Action: " + str_action_name + " : " + str_cur_line
                    # count all the DOTS to identify the parent till ROOT
                    if str_cur_line.count(".(") > 0:
                        int_cur_parent_count = len(str_cur_line.split(" ")[2].split("(")[0])
                        str_top_of_stack = str_arr_parent_ae_sqlid_name[len(str_arr_parent_ae_sqlid_name) - 1]
                        str_cur_sql_id = str_cur_line.split(" ")[2].strip(".").strip("(").strip(")")
                        # str_cur_sql_id = str_cur_line.split(" ")[2].strip(".").strip("(").strip(")").split(".")
                        # str_cur_sql_id = str_cur_sql_id[0] + "." + str_cur_sql_id[1]
                        if int_cur_parent_count + 1 > len(str_arr_parent_ae_sqlid_name):
                            str_arr_parent_ae_sqlid_name.append(str_cur_sql_id)
                        elif int_cur_parent_count + 1 == len(str_arr_parent_ae_sqlid_name):
                            str_arr_parent_ae_sqlid_name.pop(-1)
                            str_arr_parent_ae_sqlid_name.append(str_cur_sql_id)
                        else:
                            str_arr_parent_ae_sqlid_name.pop(-1)
                            str_arr_parent_ae_sqlid_name.pop(-1)
                            str_arr_parent_ae_sqlid_name.append(str_cur_sql_id)
                            
                    str_org_action_name = str_action_name
                    if "Call Section" in str_action_name:
                        str_action_name = "SQL"
                    # print str(str_arr_parent_ae_sqlid_name).replace(",", " --> ") + " --> " + str_org_action_name
                    # itr_set_lines = lst_avlbl_actns.get(str_action_name, actn_not_found)(str_cur_line, itr_set_lines, dict_AET_prcs_dtls, int_ln_indx, str_org_action_name, insert_rows)
                    lst_avlbl_actns.get(str_action_name, actn_not_found)(str_cur_line, itr_set_lines, dict_AET_prcs_dtls, int_ln_indx, str_org_action_name, insert_rows)
                    if int_ln_indx % 10000 == 0:
                        print "Lines processed from file: " + str(int_total_ln_indx)
                        db_con.commit()
    db_con.commit()

def insert_into_db(cur, insert_rows):
    """Insert the collected data into the database table."""
    # print str(insert_rows)
    # Special handling for CLOB data type
    # str_sql_stmt = cur.var(cx_Oracle.CLOB)
    # str_sql_stmt.setvalue(0, insert_rows[17])
    # Insert into SQL Table
    # Original statement WORKS!
    # cur.execute("INSERT INTO PSPPPARSEAET (PROCESS_INSTANCE, SEQ_NBR, AE_APPLID, SQLID, PM_SQL_TYPE, COUNTER, SQLROWS_2, START_TIME, END_TIME, CALC_TIME, SQLTEXT2) values (:1, :2, :3, :4, :5, :6, :7, TO_TIMESTAMP(:8, 'HH24:MI:SS.FF'), TO_TIMESTAMP(:9, 'HH24:MI:SS.FF'), TO_TIMESTAMP(:10, 'HH24:MI:SS.FF'), :11)", [insert_rows[0], insert_rows[1], insert_rows[2], insert_rows[3], insert_rows[4], insert_rows[5], insert_rows[6], insert_rows[7], insert_rows[8], insert_rows[9], str_sql_stmt])
    # str_array_sql_stmt = [insert_rows[0], insert_rows[1], insert_rows[2], insert_rows[3], insert_rows[4], insert_rows[5], insert_rows[6], insert_rows[7], insert_rows[8], insert_rows[9], insert_rows[10], insert_rows[11], insert_rows[12], insert_rows[13], insert_rows[14], insert_rows[15], insert_rows[16], str_sql_stmt]
    # print "Insert Stmt " + str(str_array_sql_stmt)
    # print "Cur.desc " + str(cur.description)
    cur.execute("INSERT INTO PSPPPARSEAET (PROCESS_INSTANCE, SEQ_NBR, AERP, AE_APPLID, SQLID, ACTION_PLAN_DESCR, PM_SQL_TYPE, PF_ITERATION_NBR, COUNTER, SQLROWS_2, DP_RESTART_CONTROL, COMMIT_ACTN_STRNG, START_TIME, END_TIME, CALC_TIME, FIELD_LIST_AET, BINDNAME, SQLTEXT2, AE_RUN_DATA) VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, TIMESTAMP(:13, 'HH24:MI:SS.FF'), TIMESTAMP(:14, 'HH24:MI:SS.FF'), TIMESTAMP(:15, 'HH24:MI:SS.FF'), :16, :17, :18, :19)", [insert_rows[0], insert_rows[1], insert_rows[2], insert_rows[3], insert_rows[4], insert_rows[5], insert_rows[6], insert_rows[7], insert_rows[8], insert_rows[9], insert_rows[10], insert_rows[11], insert_rows[12], insert_rows[13], insert_rows[14], insert_rows[15], insert_rows[16], insert_rows[17], insert_rows[18]])
						
def main():
    """The main function from where the processing starts."""

    str_net_start_time = datetime.datetime.utcnow()
    global bool_negative_row_delete
    # mypath = dirname(realpath(__file__))
    mypath = "D:\\PP_Oracle\\1_Work\\FSCM\\Bugs\\AETFiles"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    int_AET_processed = 0
    
    for file in onlyfiles:
        if file != basename(__file__) and file.endswith("AET"):
            # Count AET files processed
            int_AET_processed += 1
            # Create Connection. This is my local DB
            db_con = sqlite3.connect('example.db')
            # Create Cursor
            cur = db_con.cursor()

            srcFileName = join(mypath, file)
            str_start_time = datetime.datetime.utcnow()
            statinfo = os.stat(srcFileName)
            with open(srcFileName) as f:
                print "Total Lines in the File : " + str(sum(1 for _ in f))
            print "Processing '" + basename(srcFileName) + "'" + ": File Size in M Bytes : " + str(statinfo.st_size/(1024*1024)) + " : Start Time : " + str(str_start_time)
            str_file_name = srcFileName
            int_prcs_inst = get_prcs_inst(basename(str_file_name))
            # print "Process instance: " + str(int_prcs_inst)
            # Before every run, make sure you delete rows for that Process Instance
            cur.execute("DELETE FROM PSPPPARSEAET WHERE PROCESS_INSTANCE = " + int_prcs_inst)
            db_con.commit()

            dict_AET_prcs_dtls = {}
            dict_AET_prcs_dtls["Summary"] = "This is autogenerated using ReadPSAET python program"
            dict_AET_prcs_dtls["Instance"] = int_prcs_inst
            dict_AET_prcs_dtls["Name"] = basename(str_file_name).split(int_prcs_inst)[0][3:].strip("_")
            # read_AET(int_prcs_inst, str_file_name, dict_AET_prcs_dtls)
            # declare variables for parallel processing
            prll_prcs = []
            int_prcs_count = 0
            # How many python processes you want to run. Make sure you check your CPU usage...
            int_total_prcs = 5
            with open(str_file_name, 'r') as infile:
                int_row_count = 0
                int_ln_indx = 0
                while(True):
                    lst_lines = list(islice(infile, 200000)) # This is the number of lines python will read in one set...
                    if  len(lst_lines) == 0:
                        break
                    # read the last line of the list
                    last_line = lst_lines[len(lst_lines) - 1].rstrip('\n')
                    while (len(last_line) != 0):
                        tmp_lst_line = list(islice(infile, 1))
                        if len(tmp_lst_line) == 0:
                            break
                        lst_lines.append(tmp_lst_line[0])
                        last_line = lst_lines[len(lst_lines) - 1].rstrip('\n')
                    try:
                        # print "Total lines Before processAETSet : " + str(len(lst_lines))
                        # processAETSet(int_prcs_inst, lst_lines, int_ln_indx)
                        p = Process(target=processAETSet, args=(int_prcs_inst, lst_lines, int_ln_indx,))
                        int_prcs_count += 1
                        p.start()
                        prll_prcs.append(p)
						# Here we check how many processes have been triggered
                        if int_prcs_count >= int_total_prcs:
                            int_prcs_count = 0
                            for prcs in prll_prcs:
                               prcs.join()
                            db_con.commit()
                            prll_prcs = []
                        int_ln_indx += (len(lst_lines) - 1)
                    except StopIteration as e:
                        print "Set completed...."
                        # break
            print "Waiting for process to complete..."
            # this is needed as the last set could be less than int_total_prcs. The join here makes sure all processes run to success and only then reads the next line of code...
            for prcs in prll_prcs:
                prcs.join()
            db_con.commit()
            # print json.dumps(dict_AET_prcs_dtls, sort_keys=False, indent=2)
            # Add UPDATE statements here. This is needed as ReUse actions need special handling
            str_sql_stmt = """UPDATE PSPPPARSEAET A
                                SET A.PM_SQL_TYPE = NVL(
                                  (SELECT PM_SQL_TYPE
                                  FROM PSPPPARSEAET B
                                  WHERE A.PROCESS_INSTANCE = B.PROCESS_INSTANCE
                                  AND A.AE_APPLID          = B.AE_APPLID
                                  AND A.SQLID              = B.SQLID
                                  --AND B.PM_SQL_TYPE       <> ' '
                                  AND B.ACTION_PLAN_DESCR  = A.ACTION_PLAN_DESCR
                                  AND B.SEQ_NBR            =
                                    (SELECT MIN(C.SEQ_NBR)
                                    FROM PSPPPARSEAET C
                                    WHERE C.PROCESS_INSTANCE = B.PROCESS_INSTANCE
                                    AND C.AE_APPLID          = B.AE_APPLID
                                    AND C.SQLID              = B.SQLID
                                    AND C.ACTION_PLAN_DESCR  = B.ACTION_PLAN_DESCR
                                 -- AND C.PM_SQL_TYPE        = B.PM_SQL_TYPE
                                    )
                                  ), 'Not Found')
                                WHERE PROCESS_INSTANCE = :prcs_inst
                                  AND PM_SQL_TYPE = ' '"""
            # UPDATE statement for END_TIME 
            str_end_time_sql_stmt = """UPDATE PSPPPARSEAET A SET END_TIME = (SELECT START_TIME FROM PSPPPARSEAET B WHERE A.PROCESS_INSTANCE = B.PROCESS_INSTANCE 
                                       AND B.SEQ_NBR = (SELECT MIN(C.SEQ_NBR) FROM PSPPPARSEAET C WHERE A.PROCESS_INSTANCE = C.PROCESS_INSTANCE AND A.SEQ_NBR < C.SEQ_NBR)) 
                                       WHERE PROCESS_INSTANCE = :prcs_inst"""
            # UPDATE statement for calculating CALC_TIME
            str_calc_time_sql_stmt = """UPDATE PSPPPARSEAET A SET CALC_TIME = (START_TIME - END_TIME) WHERE PROCESS_INSTANCE = :prcs_inst"""
            # cur.execute(str_sql_stmt, {"prcs_inst": int_prcs_inst})
            # cur.execute(str_end_time_sql_stmt, {"prcs_inst": int_prcs_inst})
            # cur.execute(str_calc_time_sql_stmt, {"prcs_inst": int_prcs_inst})
            db_con.commit()
            cur.close()
            db_con.close()
            str_end_time = datetime.datetime.utcnow()
            # Log Findings
            if bool_negative_row_delete:
                print "AET file '" + basename(srcFileName) + "' has Row(s) affected = -1"
            # Log time taken for each file 
            print "Total time taken '" + basename(srcFileName) + "' : " + str(str_end_time - str_start_time) + " second(s)"
            print "-----------------------------------------------------------------------------------------------------------------------------"

    str_net_end_time = datetime.datetime.utcnow()
    # Log total time taken for all files
    print "Total time taken for " + str(int_AET_processed)  + " AET files is " + str(str_net_end_time - str_net_start_time) + " second(s)"
if __name__ == "__main__":
    main()
    