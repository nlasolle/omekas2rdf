from rdflib import Namespace

RESULTS_PER_PAGE = 500
FORMAT = "turtle" #Options: {"rdfxml", "jsonld", "turtle", "ntriples"}

#Path for API call
API_PATH = "http://henripoincare.fr/api/"
ITEMS = "items" # API_PATH + ITEMS for getting all items
MEDIAS = "media"
COLLECTIONS = "item_sets"
VOCABULARIES = "vocabularies"

#Files management
MAX_DAYS = 7 #Number of days to keep backup files (.log and .ttl files)
#FILES_REPOSITORY = "/var/lib/rdf_db_hp/"
#BACKUP_REPOSITORY = "/opt/backup/rdf_db_hp/"
#LOGS_REPOSITORY = "/var/lib/rdf_db_hp/logs/"
FILES_REPOSITORY = "./rdf_db_hp/"
BACKUP_REPOSITORY = "./rdf_db_hp/"
LOGS_REPOSITORY = "./logs/"
ITEMS_FILE = "items.ttl"
MEDIAS_FILE = "medias.ttl"
COLLECTIONS_FILE = "collections.ttl"

#Prefixes which will store prefixes with RDF namespaces by calling Omeka S vocabularies API
namespaces = {}

#Omeka related namespaces (added for quick access)
O = Namespace("http://omeka.org/s/vocabs/o#")
O_CNT = Namespace("http://www.w3.org/2011/content#")