import os
import os.path

from pipeline.utils import load_json

from rdflib import Graph, Namespace, Literal, URIRef, BNode
from rdflib.collection import Collection
from rdflib.namespace import FOAF, RDF, RDFS, OWL, XSD
from typing import List, Dict

class OWLSchemaBuilder(object):
    def __init__(self, schema_file_path:str, root_path:str):
        _relative_path_without_extension = schema_file_path[len(root_path)+1:].replace(".schema.omi.json", "").split("/")
        self.version = _relative_path_without_extension[0]
        self.relative_path_without_extension = _relative_path_without_extension[1:]
        self.graph = Graph()
        self.properties_file = load_json(os.path.join(os.path.realpath("."), "sources", "vocab", "properties.json"))
        self._schema_payload = load_json(schema_file_path)
        self.class_uri = URIRef(self._schema_payload["_type"])

    def _target_file_without_extension(self) -> str:
        return os.path.join(self.version, "/".join(self.relative_path_without_extension))

    def _restriction_mutiple_range(self, prop_uri:URIRef, prop_range:List, prop_spec:Dict, required:bool):
        restriction = BNode()
        self.graph.add((self.class_uri, RDFS.subClassOf, restriction))
        self.graph.add((restriction, RDF.type, OWL.Restriction))
        self.graph.add((restriction, OWL.onProperty, prop_uri))
        if len(prop_range) == 1:
            self.graph.add((restriction, OWL.allValuesFrom, URIRef(prop_range[0])))
        else:
            all_values_from = BNode()
            self.graph.add((restriction, OWL.allValuesFrom, all_values_from))
            union_list_node = BNode()
            Collection(self.graph, union_list_node, [URIRef(embedded_type) for embedded_type in prop_range])
            self.graph.add((all_values_from, RDF.type, OWL.Class))
            self.graph.add((all_values_from, OWL.unionOf, union_list_node))
        if ('type' in prop_spec and prop_spec['type'] != 'array') or ('type' not in prop_spec):
            self.graph.add((restriction, OWL.maxCardinality, Literal(1, datatype=XSD.nonNegativeInteger)))
        #elif ('type' in prop_spec and prop_spec['type'] != 'array') and (len(linked_types := prop_spec.get('_linkedTypes') or []) == 1 or len(embedded_types := prop_spec.get('_embeddedTypes') or []) == 1):
        #    self.graph.add((prop_uri, RDFS.range, URIRef((linked_types or embedded_types)[0])))

        if required:
            self.graph.add((self.class_uri, RDFS.subClassOf, restriction))
            self.graph.add((restriction, RDF.type, OWL.Restriction))
            self.graph.add((restriction, OWL.onProperty, URIRef(prop_uri)))
            self.graph.add((restriction, OWL.minCardinality, Literal(1, datatype=XSD.nonNegativeInteger)))

    def _translate_property_specifications(self, prop_uri:URIRef, prop_spec:Dict, required:bool):
        prop_uri = URIRef(prop_uri)
        if '_linkedTypes' in prop_spec:
            self.graph.add((prop_uri, RDF.type, OWL.ObjectProperty))
            self._restriction_mutiple_range(prop_uri, prop_spec['_linkedTypes'], prop_spec, required)

        elif '_embeddedTypes' in prop_spec:
            self.graph.add((prop_uri, RDF.type, OWL.ObjectProperty))
            self._restriction_mutiple_range(prop_uri, prop_spec['_embeddedTypes'], prop_spec, required)

        elif 'type' in prop_spec and prop_spec['type'] in ['string', 'number', 'array']:
            self.graph.add((prop_uri, RDF.type, OWL.DatatypeProperty))
            if prop_spec['type'] == 'string':
                # TODO include list of _formats and other datatypes
                if '_formats' in prop_spec and 'date' in prop_spec['_formats'] and len(prop_spec['_formats']) == 1:
                    self.graph.add((prop_uri, RDFS.range, XSD.date))
                else: # IRI not represented in OWL as datatype (xsd:anyURI not suitable)
                    self.graph.add((prop_uri, RDFS.range, XSD.string))
            elif prop_spec['type'] == 'number':
                self.graph.add((prop_uri, RDFS.range, XSD.decimal))
            elif prop_spec['type'] == 'array':
               self.graph.add((prop_uri, RDFS.range, RDF.List))
               restriction = BNode()
               self.graph.add((self.class_uri, RDFS.subClassOf, restriction))
               self.graph.add((restriction, RDF.type, OWL.Restriction))
               self.graph.add((restriction, OWL.onProperty, prop_uri))
               self.graph.add((restriction, OWL.maxCardinality, Literal(1, datatype=XSD.nonNegativeInteger)))

            if required:
                restriction = BNode()
                self.graph.add((self.class_uri, RDFS.subClassOf, restriction))
                self.graph.add((restriction, RDF.type, OWL.Restriction))
                self.graph.add((restriction, OWL.onProperty, URIRef(prop_uri)))
                self.graph.add((restriction, OWL.minCardinality, Literal(1, datatype=XSD.nonNegativeInteger)))
            pass

        self.graph.add((prop_uri, RDFS.label, Literal(prop_spec['label'])))
        if 'description' in prop_spec:
            self.graph.add((prop_uri, RDFS.comment, Literal(prop_spec['description'])))
        #self.graph.add((prop_uri, FOAF.name, Literal(prop_spec['name'])))

        return

    def translate(self):
        self.graph.add((self.class_uri, RDF.type, OWL.Class))
        self.graph.add((self.class_uri, RDFS.label, Literal(self._schema_payload['label'])))
        if 'description' in self._schema_payload:
            self.graph.add((self.class_uri, RDFS.comment, Literal(self._schema_payload['description'])))
        #self.graph.add((self.class_uri, FOAF.name, Literal(self._schema_payload['name'])))

        if "properties" in self._schema_payload and self._schema_payload["properties"]:
            for prop_uri, prop_spec in self._schema_payload['properties'].items():
                required = False
                if "required" in self._schema_payload and self._schema_payload["required"]:
                    if prop_uri in self._schema_payload['required']:
                        required=True
                self._translate_property_specifications(prop_uri, prop_spec, required)

                #self.graph.add((URIRef(prop_uri), RDFS.domain, OWL.Thing))
                if prop_uri.split('/')[-1] in self.properties_file:
                    # property rdfs:domain
                    if len(self.properties_file[prop_uri.split('/')[-1]]['usedIn'][self.version]) > 1:
                        property_domain = BNode()
                        self.graph.add((URIRef(prop_uri), RDFS.domain, property_domain))
                        union_list_node = BNode()
                        Collection(self.graph, union_list_node, [URIRef(domain_type) for domain_type in self.properties_file[prop_uri.split('/')[-1]]['usedIn'][self.version]])
                        self.graph.add((property_domain, RDF.type, OWL.Class))
                        self.graph.add((property_domain, OWL.unionOf, union_list_node))
                    else:
                        self.graph.add((URIRef(prop_uri), RDFS.domain, URIRef(self.properties_file[prop_uri.split('/')[-1]]['usedIn'][self.version][0])))
                    # property rdfs:range
                    if 'asEdge' in self.properties_file[prop_uri.split('/')[-1]] and len(self.properties_file[prop_uri.split('/')[-1]]['asEdge']['canPointTo'].get(self.version, [])) > 1:
                        property_range = BNode()
                        self.graph.add((URIRef(prop_uri), RDFS.range, property_range))
                        union_list_node = BNode()
                        Collection(self.graph, union_list_node, [URIRef(range_type) for range_type in self.properties_file[prop_uri.split('/')[-1]]['asEdge']['canPointTo'][self.version]])
                        self.graph.add((property_range, RDF.type, OWL.Class))
                        self.graph.add((property_range, OWL.unionOf, union_list_node))
                    elif 'asEdge' in self.properties_file[prop_uri.split('/')[-1]] and self.properties_file[prop_uri.split('/')[-1]]['asEdge']['canPointTo'].get(self.version):
                        self.graph.add((URIRef(prop_uri), RDFS.range, URIRef(self.properties_file[prop_uri.split('/')[-1]]['asEdge']['canPointTo'][self.version][0])))
        return

    def build(self):
        target_file = os.path.join("target", "schemas", "Turtle", f"{self._target_file_without_extension()}.ttl")
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        self.translate()
        self.graph.serialize(destination=target_file, format="ttl")
        target_file = os.path.join("target", "schemas", "RDF-XML", f"{self._target_file_without_extension()}.xml")
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        self.graph.serialize(destination=target_file, format="xml")
        target_file = os.path.join("target", "schemas", "JSON-LD", f"{self._target_file_without_extension()}.jsonld")
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        self.graph.serialize(destination=target_file, format="json-ld")
