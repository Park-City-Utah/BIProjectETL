#Parker Ferguson
#BI ETL Project: ETL script
#Dec 26, 2013
#ETL scripting for the extraction from current database, creation of new data warehouse and transfer of data
#from database to data warehouse

from Database import *

db = ConnectToDB('localhost', 'root', 'P@ssw0rd!', 'db')

#Extraction
data = ExtractDataFromDB(db)

#Transform

#Load 
CreateDataWarehouse(db, 'dwETL')
dw = ConnectToDB('localhost', 'root', 'P@ssw0rd!', 'dwETL')
LoadDataToDB(dw, data)

##INCOMPLETE
#1	FactSession date_id and project_id LOAD
#2  Foreign constraints for project_id and date_id in factSession required POST LOAD

