import requests, json, rdflib, logging, os

from datetime import date, datetime, timedelta
from zipfile import ZipFile
from triplesCreation import *
from constants import *


def alterFilesPermissions():
	#RDF files
	for r, d, f in os.walk(FILES_REPOSITORY):
		for file in f:
			try:
				filePath = os.path.join(r, file)
				os.chmod(filePath, 0777)
			except:
				logging.exception("Permission update execpetion: ", exc_info=True)
				next



#Create a backup archive containing current RDF base content
def createBackup():
	yesterday = datetime.now() - timedelta(days=1)

	#Create archive file
	archiveFile = BACKUP_REPOSITORY + yesterday.strftime("%Y%m%d") + "_base_rdf" + ".zip"

	#Add all RDF files to the archive (see https://docs.python.org/2.7/library/zipfile.html for documentation)
	with ZipFile(archiveFile, 'w') as zipObj:

	   # Iterate over all the files in directory
	   for r, d, f  in os.walk(FILES_REPOSITORY):
		   for file in f:
			   #create complete filepath of file in directory
			   filePath = os.path.join(r, file)

			   # Add file to zip
			   zipObj.write(filePath)

	os.chmod(archiveFile, 0777)

#Clean repository by removing X days old file (default set to 30 days)
#Log and archive files names start with the date with format "YYYYmmdd"
def cleanRepository():

	today = date.today()

	#Clean log files repository
	for r, d, f in os.walk(LOGS_REPOSITORY):
		for file in f:
			filePath = os.path.join(r, file)

			try:
				creationDate = datetime.strptime(file[:8], "%Y%m%d")
				#Remove x days old file
				if( (today - datetime.date(creationDate)).days > MAX_DAYS): 
					os.remove(os.path.join(r, file))
			except: 
				logging.exception("Exception message:", exc_info=True)
				next


	#Clean backup archives repository
	for r, d, f in os.walk(BACKUP_REPOSITORY):
		for file in f:
			filePath = os.path.join(r, file)

			try:
				creationDate = datetime.strptime(file[:8], "%Y%m%d")
				#Remove X days old file
				if( (today - datetime.date(creationDate)).days > MAX_DAYS): 
					os.remove(os.path.join(r, file))
			except:
				next
	

#Configure logger (see https://realpython.com/python-logging/ for details)
def configureLogging():
	today = date.today()

	logfile = LOGS_REPOSITORY + today.strftime("%Y%m%d_RDF_db_update") + ".log"

	logging.basicConfig(filename = logfile, 
		format='%(levelname)s - %(asctime)s - %(message)s', 
		level=logging.INFO)

	#Last log file
	os.chmod(logfile, 0777)

#Get Omeka S resource by making REST API calls 
#Save items, medias or collections to RDF base (several files)
def saveResources(category):

	graph = initializeRDFdatabase()
	callOver = False
	page = 0

	#The call is split into several pages to avoid loosing data
	while not callOver:

		#Python request package is used to make the HTTP call 
		#See https://realpython.com/python-requests/ for examples
		logging.info("Calling " + API_PATH +  category)

		stringParams = {'page' : page, 'per_page': RESULTS_PER_PAGE}
		response = requests.get(API_PATH + category, stringParams)

		#Response ok if status code between 200 and 400
		if response:
			resources = response.json()

			if len(resources) > 0:
				logging.info("Page number " + str(page) + " with " + str(len(resources)) + " resources.")
				page += 1

				if(category == ITEMS):
					createItemsTriples(resources, graph)
				elif(category == MEDIAS):
					createMediasTriples(resources, graph)
				else:
					createCollectionsTriples(resources, graph)
			else:
				callOver = True
				logging.info("No further data to fetch. Call is over for " + str(category) + ".")
		else: 
			logging.error("An error has occured. Response code: " + str(response.status_code))


	#Save graph resources to a RDF file
	saveGraphToFile(graph, category , FORMAT);


#Main program


#Add backup archive and remove old files

createBackup()
cleanRepository()

#Instanciate and configure a logger
configureLogging()

logging.info("RDF database update initialization.")

logging.info("Starting items creation.")
saveResources(ITEMS)

logging.info("Starting medias creation.")
saveResources(MEDIAS)

logging.info("Starting collections creation.")
saveResources(COLLECTIONS)

logging.info("Updating files permissions");
alterFilesPermissions()

logging.info("RDF database successfully updated.")