import requests, json, rdflib, sys, logging

from rdflib import Graph, RDF, RDFS, URIRef, Literal, Namespace
from rdflib.namespace import XSD
from constants import *

#RDFLib library is used to create the RDF document (in Turtle syntax)
#Go here to find more details: https://rdflib.readthedocs.io/en/stable/gettingstarted.html
def initializeRDFdatabase():
	logging.info("Adding namespaces to the RDF graph")

	#Initializes the RDF graph
	graph = Graph()

	#Add defined namespaces to the graph
	for key, value in namespaces.items():
		graph.bind(key, value)

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
		

			#All properties
			for key in item:
				#2 conditions are required to save only required property and values
				#The first thing to check is that the format of the key is "prefix:value" (ex. dcterms:subject)
				#The second thing is to avoid saving Omeka S related content (ex. "o:resource_class")
				#if only retrieve (isinstance(item[key], list) and 
				if ":" in key and not key.startswith("o:"):
					for element in item[key]: 
						
						#Omeka returns predicate under the form "prefix:value" (ex. dcterms:subject)
						#But  RDFlib method needs the full URI to create the RDF node (ex. http://purl.org/dc/terms/subject )
						#which is part of a triple (prefixes given as keys of json resources)

						prefix = key[0:key.index(":")]
						if len(prefix) > 0:
							predicate = URIRef(namespaces[prefix] + key[len(prefix) + 1:])
							if "@value" in element:
								graph.add( (uri, predicate, Literal(element["@value"])) )
							
							if "@id" in element:
								if element["@id"].strip().startswith("http"):
									graph.add( (uri, predicate, URIRef(element["@id"].strip())) )
								else:
									graph.add( (uri, predicate, Literal(element["@id"].strip())) )
					
							
			# We want to save the type associated with items,
			# but not saving that every item is an Omeka item (o:item)
			for type in item["@type"]:
				if ":" in type and not type.startswith("o:"):
					prefix = type[0:type.index(":")]
					if len(prefix) > 0:
						object = URIRef(namespaces[prefix] + type[len(prefix) + 1:])
						graph.add( (uri, RDF.type, object) )

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


			except: 
				logging.exception("An error occured for media with id: " + str(media["@id"]))
				logging.exception("Exception message:", exc_info=True)
				continue #Go to next media


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
				continue #Go to next collection
