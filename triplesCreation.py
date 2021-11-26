import requests, json, rdflib, sys, logging

from rdflib import Graph, RDF, RDFS, URIRef, Literal, Namespace
from rdflib.namespace import XSD
from constants import *

#RDFLib library is used to create the RDF document (in Turtle syntax)
#Go here to find more details: https://rdflib.readthedocs.io/en/stable/gettingstarted.html
def initializeRDFdatabase():
	logging.info("Adding namespaces to RDF database")

	graph = Graph()

	#Add namespaces
	graph.bind("ahpo", AHPO)
	graph.bind("o", O)
	graph.bind("bio", BIO)
	graph.bind("dcterms", DCTERMS)
	graph.bind("rel", REL)
	graph.bind("o-cnt", O_CNT)
	graph.bind("hp", HP)

	return graph

#Save an RDF graph to a file of one of the specified format (RDF/XML, turtle, etc.)
def saveGraphToFile(graph, category, format):

	#Get the name of the file to 
	if category == ITEMS:
		file = FILES_REPOSITORY + ITEMS_FILE
	elif category == MEDIAS:
		file = FILES_REPOSITORY + MEDIAS_FILE
	else:
		file = FILES_REPOSITORY + COLLECTIONS_FILE

	logging.info("Saving graph to file " + file + " using " + FORMAT + " serialization.")

	try:
		graph.serialize(destination = file, format = format)
	except: 
		logging.exception("An error occured during the creation of the RDF file: " + file)
		logging.exception("Exception message:", exc_info=True)

#Add the given items to the RDF database by creating appropriate triples
def createItemsTriples(items, graph):

	graph.add( (AHPO.sentBy, RDFS.subPropertyOf, HP.correspondant) );
	graph.add( (AHPO.sentTo, RDFS.subPropertyOf, HP.correspondant) );
	graph.add( (AHPO.DestinationAddress, HP.nicename, Literal("adresse")) );
	graph.add( (AHPO.Person, HP.nicename, Literal("individu")) );
	graph.add( (AHPO.Article, HP.nicename, Literal("article")) );
	graph.add( (AHPO.BookChapter, HP.nicename, Literal("chapitre")) );
	graph.add( (AHPO.Report, HP.nicename, Literal("rapport")) );
	graph.add( (AHPO.Book, HP.nicename, Literal("livre")) );
	graph.add( (AHPO.Thesis, HP.nicename, Literal("these")) );
	graph.add( (AHPO.Journal, HP.nicename, Literal("journal")) );
	graph.add( (AHPO.Issue, HP.nicename, Literal("publication")) );
	graph.add( (AHPO.Letter, HP.nicename, Literal("lettre")) );

	for item in items:
		try:
			#The uri
			uri = URIRef(item["@id"])

			#The label
			graph.add( (uri, RDFS.label, Literal(item["o:title"])) )

			#A resource may be part of several item sets
			if "o:item_set" in item:
				for item_set in item["o:item_set"]:
					graph.add( (uri, O.item_set, URIRef(item_set["@id"].strip())) )

			if "ahpo:writingDate" in item:
				for date in item["ahpo:writingDate"]:
					fullDate = date["@value"];
					graph.add( (uri, HP.created, Literal(fullDate) ))
					graph.add( (uri, HP.year, Literal(fullDate[:4], datatype=XSD.integer)) )

	
			graph.add( (uri, HP.link, Literal("http://henripoincare.fr/s/correspondance/item/" + str(item["o:id"]))) )
			#Every item is an omeka item
			#graph.add( (uri, RDF.type, O.Item) )

			#The differents classes
			for type in item["@type"]:
				#Only save ahpo class
				if("ahpo" in type):
					object = AHPO + type[5:]
					graph.add( (uri, RDF.type, URIRef(object)) )

			#All other items are included
			for key in item:
				if(isinstance(item[key], list)):
					for element in item[key]: 
						if("ahpo" in key):
							predicate = URIRef(AHPO + key[5:]) # RDFlib method needs the full URI to create the triple (prefixes given as keys of json resources)
						elif("rel" in key):
							predicate = URIRef(REL + key[4:])
						elif("bio" in key):
							predicate = URIRef(BIO + key[4:])
						elif("dcterms" in key):
							predicate = URIRef(DCTERMS + key[8:])
						elif("hp" in key):
							predicate = URIRef(DCTERMS + key[3:])
						elif("o" in key):
							predicate = URIRef(O + key[2:])

						if "@value" in element:
							graph.add( (uri, predicate, Literal(element["@value"])) )

						if "@id" in element:
							graph.add( (uri, predicate, URIRef(element["@id"].strip())) )



		except: 
			logging.exception("An error occured for item with id: " + str(item["@id"]))
			logging.exception("Exception message:", exc_info=True)
			continue #Go to next item

def createMediasTriples(medias, graph):
		for media in medias:
			try:
				#The uri
				uri = URIRef(media["@id"])

				#The type 
				if "o-cnt" in media["@type"]:
					graph.add( (uri, RDF.type, URIRef(O_CNT + media["@type"][6:])))
					if "o-cnt:chars" in media:
						graph.add( (uri, O_CNT.chars, Literal(media["o-cnt:chars"])) )
				else: 
					graph.add( (uri, RDF.type, O.Media) )

				#The label
				graph.add( (uri, RDFS.label, Literal(media["o:title"])) )

				#Source (link)
				if "o:source" in media:
					graph.add( (uri, O.source, Literal(media["o:source"])) )

				#The related item
				if "o:item" in media:
					graph.add( (uri, O.item, URIRef(media["o:item"]["@id"])))

				if "ahpo:editedBy" in media:
					graph.add( (uri, AHPO.editedBy, Literal(media["ahpo:editedBy"])) )

			except: 
				logging.exception("An error occured for media with id: " + str(media["@id"]))
				logging.exception("Exception message:", exc_info=True)
				continue #Go to next item


def createCollectionsTriples(collections, graph):
	for set in collections:
			try:
				#The uri
				uri = URIRef(set["@id"])

				#The label
				graph.add( (uri, RDFS.label, Literal(set["o:title"])) )
			except: 
				logging.exception("An error occured for set with id: " + str(set["@id"]))
				logging.exception("Exception message:", exc_info=True)
				continue #Go to next item
