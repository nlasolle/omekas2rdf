# General purpose
This python script has been created for the daily export of an Omeka S database to an RDF database (Turtle syntax).

# Details about the Omeka S installation
Omeka S is a CMS (Content Management System) dedicated to the editing and the publishing of collections.
It allows to create elements and publish them on a website based on the use of blocks and modules. 
Is is particularly adapted for cultural heritage collections (museums, archive places, libraries, etc).

It is currently in use for a project dedicated to Henri Poincaré (1854-1912), famous French man of science, managed bythe Archives Henri-Poincaré laboratory.
The website is available at http://henripoincare.fr.

# Details about the script
Omeka S data can be exported through an Web API, which exports results under a JSON syntax.

This scripts makes a request to the API, filters the results (some data is related to the Omeka S environment, and does not describes the content), and save the results under the RDF formats.
 
This script also manages aspects related to our server installation, by creating backup files and saving newly created files to the appropriated repository.
Each night, the script is automaticly called to update the RDF database by integrating the potential Omeka S modifications.
A log file is also generated to save the trace of potential errors.

# What for?
Using a proper RDF database allows the use of more elaborated tools which uses the W3C standards (RDF, RDFS, OWL, SPARQL).
The RDF database can be exposed through a SPARQL endpoint.
