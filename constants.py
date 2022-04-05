from rdflib import Namespace

RESULTS_PER_PAGE = 500
FORMAT = "turtle" #Options: {"rdfxml", "jsonld", "turtle", "ntriples"}

#Path for API call
API_PATH = "http://henripoincare.fr/api/"
ITEMS = "items" # API_PATH + ITEMS for getting all items
MEDIAS = "media"
COLLECTIONS = "item_sets"

#Files management
MAX_DAYS = 7 #Number of days to keep backup files (.log and .ttl files)
FILES_REPOSITORY = "/var/base_rdf/"
BACKUP_REPOSITORY = "/opt/backup/rdf_db_hp/"
LOGS_REPOSITORY = "/var/base_rdf/logs/"
ITEMS_FILE = "items.ttl"
MEDIAS_FILE = "medias.ttl"
COLLECTIONS_FILE = "collections.ttl"

#Prefixes associated with RDF namespaces
namespaces = {
    'ahpo':'http://e-hp.ahp-numerique.fr/ahpo#',
    'ahpot' : 'http://henripoincare.fr/ahpot#',
    'bibo' : 'http://purl.org/ontology/bibo/',
    'bio' : 'http://purl.org/vocab/bio/0.1/',
    'dcterms' : 'http://purl.org/dc/terms/',
    'dctype' : 'http://purl.org/dc/dcmitype/',
    'exif' : 'http://www.w3.org/2003/12/exif/ns#',
    'fabio' : 'http://purl.org/spar/fabio/',
    'foaf' : 'http://xmlns.com/foaf/0.1/',
    'o' : 'http://omeka.org/s/vocabs/o#',
    'o_cnt' : 'http://www.w3.org/2011/content#',
    'rel' : 'http://purl.org/vocab/relationship/'
}

#Omeka related namespaces (added for quick access)
O = Namespace("http://omeka.org/s/vocabs/o#")
O_CNT = Namespace("http://www.w3.org/2011/content#")