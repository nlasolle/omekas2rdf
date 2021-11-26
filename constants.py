from rdflib import Namespace

RESULTS_PER_PAGE = 500
FORMAT = "turtle" #Options: {"rdfxml", "jsonld", "turtle", "ntriples"}

API_PATH = "http://henripoincare.fr/api/"

#Path for API call
ITEMS = "items"
MEDIAS = "media"
COLLECTIONS = "item_sets"

#Files management
MAX_DAYS = 7 #Number of days to keep backup files (.log and .ttl files)
FILES_REPOSITORY = "/var/tomcat/base_rdf/"
BACKUP_REPOSITORY = "/opt/backup/database/rdf_db_hp/"
LOGS_REPOSITORY = "/var/tomcat/logs/"
ITEMS_FILE = "items.ttl"
MEDIAS_FILE = "medias.ttl"
COLLECTIONS_FILE = "collections.ttl"

#Prefixes associated with RDF namespaces
AHPO = Namespace("http://e-hp.ahp-numerique.fr/ahpo#")
O = Namespace("http://omeka.org/s/vocabs/o#")
REL = Namespace("http://purl.org/vocab/relationship/")
BIO = Namespace("http://purl.org/vocab/bio/0.1/")
DCTERMS = Namespace("http://purl.org/dc/terms/")
O_CNT = Namespace("http://www.w3.org/2011/content#")
HP = Namespace("http://hpBase/")