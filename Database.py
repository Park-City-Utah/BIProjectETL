import mysql.connector
import sys

########connection for database creation
def ConnectToMySQL(db_host, db_user, db_pass):
    try:
        db = mysql.connector.connect(
            host = db_host,
            user = db_user,
            passwd = db_pass,
        )
        return db  
    except Exception as e:
        print("Error, connection to database failure; This is the info we have about it:" + e)
        sys.exit('Exiting')

    
###########connect to database
def ConnectToDB(db_host, db_user, db_pass, db_name):
    try:
        db = mysql.connector.connect(
            host = db_host,
            user = db_user,
            passwd = db_pass,
            db = db_name
        )
        return db  
    except Exception as e:
        print("Error, connection to database failure; This is the info we have about it:" + str(e))
        sys.exit('Exiting')  

def CreateDataBaseFromCSV(db, filename):
    cursor = db.cursor()
    # Open and read the file as a single buffer
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()

    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')

    # Execute every command from the input file
    for command in sqlCommands:
        try:
            cursor.execute(command)
            print("\nSuccess! The DataBase was created from file:" + filename + "\n")
        except Exception as e:
            print("Error, sql failure; This is the info we have about it: " + str(e))
	
    cursor.close()  
          
#datawarehouse creation
def CreateDataWarehouse(db, dw_name):
	try:
		cursor = db.cursor()
		cursor.execute("DROP DATABASE IF EXISTS " +  dw_name + ";")
		cursor.execute("CREATE DATABASE IF NOT EXISTS dwETL DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;")
		cursor.execute("USE " + dw_name + ";")	
	
	#creation of dimProject table
		cursor.execute("CREATE TABLE IF NOT EXISTS dimproject ("
	"project_id int(11) NOT NULL AUTO_INCREMENT,"
	"project_name varchar(45) NOT NULL,"
	"project_createDate datetime NOT NULL,"
	"project_completionDate datetime,"
	"project_lastActivityDate datetime,"
	"project_team_id int(11) NOT NULL,"
	"project_team_name varchar(45) NOT NULL,"
	"project_team_createDate date NOT NULL,"
	"PRIMARY KEY (project_id),"
	"KEY project_team_id (project_team_id)"
	") ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1;")
	
	#creation of dimDate table
		cursor.execute("CREATE TABLE IF NOT EXISTS dimdate ("
		"date_id int(11) NOT NULL AUTO_INCREMENT,"
		"date_day int(11) NOT NULL,"
		"date_month int(11) NOT NULL,"
		"date_year int(11) NOT NULL,"
		"date_time time NOT NULL,"
		"PRIMARY KEY (`date_id`)"
		") ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1;")

	#creation of dimLocation table
		cursor.execute("CREATE TABLE IF NOT EXISTS dimlocation ("
		"location_id int(11) NOT NULL AUTO_INCREMENT,"
		"location_country varchar(45) NOT NULL,"
		"location_subDivision varchar(45) NOT NULL,"
		"location_city varchar(45) NOT NULL,"
		"PRIMARY KEY (location_id)"
		") ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1;")

	#creation of dimUsers table
		cursor.execute("CREATE TABLE IF NOT EXISTS dimusers (user_id int(11) NOT NULL AUTO_INCREMENT,"
		"user_fName varchar(45) DEFAULT NULL,"
		"user_lName varchar(45) DEFAULT NULL,"
		"user_email varchar(45) DEFAULT NULL,"
		"user_gender varchar(1) DEFAULT NULL,"
		"user_dateBirth date DEFAULT NULL,"
		"user_createDate date DEFAULT NULL,"
		"user_upgradeDate date DEFAULT NULL,"
		"user_plan_id int(10) DEFAULT NULL,"
		"user_plan_name varchar(45) DEFAULT NULL,"
		"user_plan_userMax int(10) DEFAULT NULL,"
		"PRIMARY KEY (user_id),"
		"KEY user_plan_id (user_plan_id)"
		") ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=50;")

	#creation of factSession table
		cursor.execute("CREATE TABLE IF NOT EXISTS factsession ("
	"session_id int(11) NOT NULL AUTO_INCREMENT,"
	"session_loginDate datetime NOT NULL,"
	"session_logoutDate datetime NOT NULL,"
	"session_ipAddress varchar(45) NOT NULL,"
	"DimUsers_user_id int(11) NOT NULL,"
	"DimLocation_location_id int(11) NOT NULL,"
	"DimProject_project_id int(11) NOT NULL,"
	"DimDate_date_id int(11) NOT NULL,"
	"PRIMARY KEY (session_id),"
	#"CONSTRAINT factsession_ibfk_1 FOREIGN KEY (DimUsers_user_id) REFERENCES dimusers (user_id) ON UPDATE CASCADE,"
	#"CONSTRAINT factsession_ibfk_2 FOREIGN KEY (DimProject_project_id) REFERENCES dimproject (project_id) ON UPDATE CASCADE,"
	#"CONSTRAINT factsession_ibfk_3 FOREIGN KEY (DimLocation_location_id) REFERENCES dimlocation (location_id) ON UPDATE CASCADE,"
	#"CONSTRAINT factsession_ibfk_4 FOREIGN KEY (DimDate_date_id) REFERENCES dimdate (date_id) ON UPDATE CASCADE,"
	"KEY DimUsers_userId (DimUsers_user_id,DimProject_project_id),"
	"KEY DimProject_projectId (DimProject_project_id),"
	"KEY session_sessionIpAddress (DimLocation_location_id),"
	"KEY dateId (DimDate_date_id)"
	") ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1;")
		
		db.commit()
		print("\nSuccess! The data warehouse has been created\n")
	except Exception as e:
		print("Error, data warehouse creation failure; This is the info we have about it:" + e)
		db.rollback()				#rollback on failure
		sys.exit('Exiting')
		
	cursor.close()   

#Extract data from Database for export to DataWarehouse
def ExtractDataFromDB(db):
    try:
        #extract data for dimUsers in data warehouse (users JOIN plan)
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users u JOIN plan p on u.Plan_plan_id = p.plan_id;")	
        userrows = cursor.fetchall()

        if userrows:
            print("\ndimUsers:")
            for row in userrows:
                print(str(row) + "\t")
    except Exception as e:
        print("Error, database extraction and print(Users) failure; This is the info we have about it:" + e)
        db.rollback()				#rollback on failure
        sys.exit('Exiting')
    print("Success! database data extraction (Users) successful")
        
    #extract data for dimLocation in data warehouse (location)
    try:
        cursor.execute("SELECT * FROM location;")	#data for dimLocation in data warehouse (location)
        locationrows = cursor.fetchall()	

        if locationrows:
            print("\ndimLocation:")
            for row in locationrows:
                print(str(row) + "\t")
    except Exception as e:
        print("Error, database extraction and print (Location) failure; This is the info we have about it:" + e)
        db.rollback()				#rollback on failure
        sys.exit('Exiting')	
    print("Success! database data extraction (Location) successful")

    #extract data for dimProject in data warehouse (project JOIN team)
    try:
        cursor.execute("SELECT p.project_id, p.project_name, p.project_createDate, p.project_completionDate, p.project_lastActivityDate, t.team_id, t.team_name, t.team_createDate FROM project p JOIN team t on p.Team_team_id = t.team_id;")	#data for dimLocation in data warehouse (location)
        projectrows = cursor.fetchall()	

        if projectrows:
            print("\ndimProject:")
            for row in projectrows:
                print(str(row) + "\t")
    except Exception as e:
        print("Error, database extraction and print(Project) failure; This is the info we have about it:" + e)
        db.rollback()				#rollback on failure
        sys.exit('Exiting')

    print("Success! database data extraction (Project) successful")
    print	

    #extract data for dimProject in data warehouse (project JOIN team)
    try:
        cursor.execute("SELECT  * FROM session;")	#data for dimLocation in data warehouse (location)
        sessionrows = cursor.fetchall()	

        if sessionrows:
            print("\ndimSession:")
            for row in sessionrows:
                print(str(row) + "\t")
    except Exception as e:
        print("Error, database extraction and print(Session) failure; This is the info we have about it:" + e)
        db.rollback()				#rollback on failure
        sys.exit('Exiting')

    print("Success! database data extraction (Session) successful")

    #extract data for dimDate in data warehouse (SessionDate for both login AND logout)
    try:
        cursor.execute("SELECT distinct day(session_loginDate),  month(session_loginDate), year(session_loginDate), time(session_loginDate) FROM Session;")	#data for both login and logout data... both will be added to warehouse
        loginDateRows = cursor.fetchall()	

        if loginDateRows:
            print("\ndimDate_Login:")
            for row in loginDateRows:
                print(str(row) + "\t")
                
        cursor.execute("SELECT distinct day(session_logoutDate), month(session_logoutDate),year(session_logoutDate), time(session_logoutDate) FROM Session;")	#data for  logout date... both will be added to warehouse
        logoutDateRows = cursor.fetchall()	

        if logoutDateRows:
            print("\ndimDate_Logout:")
            for row in logoutDateRows:
                print(str(row) + "\t")
    except Exception as e:
        print("Error, database extraction and print(Date) failure; This is the info we have about it:" + e)
        db.rollback()				#rollback on failure
        sys.exit('Exiting')
    print("Success! database data extraction (Date) successful")

    #close connection to database
    cursor.close()	

    data = [userrows, locationrows, projectrows, sessionrows, loginDateRows, logoutDateRows]
    return data

def LoadDataToDB(db, data):
    userRows = data[0]
    locationRows = data[1]
    projectRows = data[2]
    sessionRows = data[3]
    loginDateRows = data[4]
    logoutDateRows = data[5]

    #######LOAD dimUsers data into data warehouse#########################
    cursor = db.cursor()
    try:
        if userRows:
            for row in userRows:
                #cursor.execute("Insert INTO fact session (DimUsers_user_id) VALUES (%s)", [row[0]])	
                cursor.execute("INSERT INTO dimUsers (user_id, user_fName, user_lName, user_email, user_gender, user_dateBirth, user_createDate, user_upgradeDate, user_plan_id, user_plan_name, user_plan_userMax)"
                                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[9], row[10], row[11]])	#note: row[8] is a duplicate of plan_id from joining
    except Exception as e:
        print("Error, LOAD Users data into data warehouse failure; This is the info we have about it:" + e)
        db.rollback()	
        sys.exit('Exiting')
    db.commit()
    print("Success! LOAD  data (Users) into data warehouse (dimUsers) successful")

    #######LOAD dimLocation data into data warehouse####################
    try:
        if locationRows:
            for row in locationRows:
                cursor.execute("INSERT INTO dimLocation (location_id, location_country, location_subDivision, location_city) "
                                "VALUES (%s, %s, %s, %s);", [row[0], row[1] , row[2], row[3]])
    except Exception as e:
        print("Error, LOAD Location data into data warehouse failure; This is the info we have about it:" + e)
        db.rollback()	
        sys.exit('Exiting')
    db.commit()
    print("Success! LOAD  data (Location) into data warehouse (dimLocation) successful")

    ######LOAD dimProject data into data warehouse#########################
    try:
        if projectRows:
            for row in projectRows:
                cursor.execute("INSERT INTO dimProject (project_id, project_name, project_createDate, project_completionDate, project_lastActivityDate, project_team_id, project_team_name, project_team_createDate)"
                                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s);", [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]])					
    except Exception as e:
        print("Error, LOAD Project data into data warehouse failure; This is the info we have about it: " + e)
        print
        db.rollback()
        sys.exit('Exiting')
    db.commit()
    print("Success! LOAD  data (Project) into data warehouse (dimProject) successful")

    #######LOAD dimDate data into data warehouse####################
    #note: we draw two streams; one for loginDate and one for logoutDate
    #date_id is auto incremented since we are using two columns of same date table, we cannot use their ids
    try:
        if loginDateRows:#login stream
            for row in loginDateRows:
                cursor.execute("INSERT INTO dimDate (date_day, date_month, date_year, date_time) "
                                "VALUES ( %s, %s, %s, %s);", [row[0], row[1] , row[2], row[3]])
        if logoutDateRows:#logout stream
            for row in logoutDateRows:
                cursor.execute("INSERT INTO dimDate (date_day, date_month, date_year, date_time) "
                                "VALUES ( %s, %s, %s, %s);", [row[0], row[1] , row[2], row[3]])
    except Exception as e:
        print("Error, LOAD date data into data warehouse failure; This is the info we have about it:" + e)
        db.rollback()	
        sys.exit('Exiting')
    db.commit()
    print("Success! LOAD  data (Date) into data warehouse (dimDate) successful")
    print

    ########LOAD factSession into data warehouse######
    #note: 0's used to fill DimLocation_location_id and DimDate_date_id; accurate way of linking required
    try:
        if sessionRows:#login stream
            for row in sessionRows:
                cursor.execute("INSERT INTO factSession (session_id, session_loginDate, session_logoutDate, session_ipAddress, DimUsers_user_id, DimLocation_location_id, DimProject_project_id, DimDate_date_id ) "
                                "VALUES (  %s, %s, %s, %s, %s, %s, 0, 0);", [row[0], row[1] , row[2], row[3], row[4], row[5]])#0, 0 into dimProject and dimDate for now
    except Exception as e:
        print("Error, LOAD session data into data warehouse failure; This is the info we have about it:" + e)
        db.rollback()	
        sys.exit('Exiting')
    db.commit()
    print("Success! LOAD  data (session) into data warehouse (factSession) successful")

    #Add foreign constraints to factSession, must be post-LOAD
    #dimProject and dimDate constraints are not YET added, need a means to link session to dimDate and dimLocation
    #"ADD CONSTRAINT factsession_ibfk_2 FOREIGN KEY (DimProject_project_id) REFERENCES dimproject (project_id) ON UPDATE CASCADE,ADD CONSTRAINT factsession_ibfk_4 FOREIGN KEY (DimDate_date_id) REFERENCES dimdate (date_id) ON UPDATE CASCADE"
    try:
        cursor.execute("ALTER TABLE factsession ADD CONSTRAINT factsession_ibfk_1 FOREIGN KEY (DimUsers_user_id) REFERENCES dimusers (user_id) ON UPDATE CASCADE, ADD CONSTRAINT factsession_ibfk_3 FOREIGN KEY (DimLocation_location_id) REFERENCES dimlocation (location_id) ON UPDATE CASCADE;")
    except Exception as e:
        print("Error, ADD CONSTRAINT fail; This is the info we have about it:" + e)
        print
        db.rollback()	
        sys.exit('Exiting')
    db.commit()
    ###########################################3

    cursor.close()		#close connection to data warehouse
    db.close()			#close db connection