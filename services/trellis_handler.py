import requests

class TrellisHandler:

    def __init__(self, host, port, base_url):
        self.host = host
        self.port = port
        self.base_url = base_url

    def get_base_uri(self):
        return 'http://' + self.host + ':' + self.port + '/' + ((self.base_url + '/') if self.base_url is not None else '')

    def create_basic_container(self, parent_uri, container_name = None):
        payload = """
            @prefix dcterms: <http://purl.org/dc/terms/>.
            @prefix o: <http://example.org/ontology>.  
            
            <> a <http://www.w3.org/ns/ldp#Container> ;
               a <http://www.w3.org/ns/ldp#BasicContainer> ;
                 dcterms:title  \"Basic container %s\" .
        """ % container_name
        headers = {
            'Slug': container_name ,
            'Host': 'localhost:8080',
            'Accept': 'text/turtle',
            'Content-Type': 'text/turtle',
            'Link': '<http://www.w3.org/ns/ldp#BasicContainer>; rel="type"  ',
            'Content-Type': 'text/plain'
        }
        uri = self.get_base_uri() + parent_uri if parent_uri is not None else self.get_base_uri()
        response = requests.request("POST", uri, headers=headers, data=payload)
        location = response.headers['location']
        return location

    def create_property(self,parent_uri,prop):
        payload = """
            @prefix dc: <http://purl.org/dc/terms/>. 
            @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.

            <>
              a rdf:Property ;
              dc:title 'Property %s.' 
        """ % prop
        headers = {
            'Host': 'localhost:8080',
            'Link': '<http://www.w3.org/ns/ldp#Resource>; rel = "type" ',
            'Slug': prop,
            'Content-Type': 'text/turtle'
        }
        uri = self.get_base_uri() + parent_uri if parent_uri is not None else self.get_base_uri()
        response = requests.request("POST", uri, headers=headers, data=payload)
        location = response.headers['location']
        return location

    def create_instance(self,instance,instance_map):
        payload2 = "@prefix dc: <http://purl.org/dc/terms/>.\n@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.\n@prefix p: <http://hercules.org/um/en-EN/res/>.\n\n<>\na rdf:Property ;\np:name 'name';\ndc:title 'Instance %s.'" % instance.id
        payload1 = instance.generate_turtle_rdf(instance_map)
        # payload = """@prefix dc: <http://purl.org/dc/terms/>.
        #             @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.
        #             @prefix cu: <http://hercules.org/um/en-EN/res/>.
        #
        #             <>
        #                 a rdf:Property ;
        #                 a dc:title 'Instance 1. of class university."""
        # payload = "@prefix dc: <http://purl.org/dc/terms/>.\n"
        # payload += "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.\n"
        # payload += "@prefix cu: <http://hercules.org/um/en-EN/res/>.\n\n"
        # payload += "<>.\n"
        # payload += "\ta rdf:Property ;\n"
        # for p in instance.properties:
        #     payload += "\tcu:%s '%s';\n" % (p,instance.properties[p])
        # payload += "\ta dc:title 'Instance %s. of class %s.\n" % (instance.id,instance.className)

        headers = {
            'Host': 'localhost:8080',
            'Link': '<http://www.w3.org/ns/ldp#RDFSource>; rel="type"',
            'Content-Type': 'text/turtle'
        }
        uri = self.get_base_uri() + instance.className if instance.className is not None else self.get_base_uri()
        response = requests.request("POST", uri, headers=headers, data=payload1)
        location = response.headers['location']
        return location

