from models.instance import Instance
from services.uris_factory_handler import URISFactoryHandler
from services.trellis_handler import TrellisHandler
import json
import os

class DataGenerator:
    def __init__(self, file,trellis_handler,uris_factory_handler):
        self.file = file
        self.properties = {}
        self.classes = {}
        self.instances = []
        self.instancesMap = {}
        self.public_uris = {
            'properties': {},
            'entities': {},
            'instances': {}
        }
        self.private_uris = {
            'properties': {},
            'entities': {},
            'instances': {}
        }
        self.counter = 0
        self.uf = uris_factory_handler # URISFactoryHandler('http://localhost:9326/', 'hercules.org', 'um', 'en-EN')
        self.th =  trellis_handler #TrellisHandler('localhost', '8080', None)

    def __increase_counter(self):
        self.counter +=1

    def generate_sintetic_data(self):
        json_data = json.load(self.file)
        self.__iterate_instances(0,None,json_data)
        self.__insert_all_data()
        print(os.getcwd())
        #file = open('%s\data\public_uris.json'%(os.getcwd()), 'w+')
        with open('./data/public_uris.json', 'w+') as f1:
            f1.write(json.dumps(self.public_uris, indent=2))
        with open('./data/private_uris.json', 'w+') as f2:
            f2.write(json.dumps(self.private_uris, indent=2))

        #json.dump(self.private_uris, outfile)


    def __iterate_instances(self,index,parent,json_instances):
        for j_instance in json_instances:
            for i in range(j_instance['instances']):
                self.__increase_counter()
                ins = Instance(self.counter,j_instance, parent)
                ins.set_canonical_uris(self.uf.create_canonical_instance(ins))  # Aquí
                if ins.className not in self.classes:
                    self.classes[ins.className] = self.uf.create_canonical_entity(ins.className)
                for p in ins.properties:
                    if p not in self.properties:
                        self.properties[p] = self.uf.create_canonical_property(p)
                self.instances.append(ins)
                self.instancesMap[ins.id] = ins
                #print(ins)
                if parent is not None:
                    parent.add_child(ins)
                if 'child' in j_instance:
                    self.__iterate_instances(self.counter,ins,j_instance['child'])


    def __insert_all_data(self):
        self.__insert_all_properties()
        self.__insert_all_entities()
        self.__insert_all_instances()


    def __insert_all_properties(self):
        self.th.create_basic_container(None, 'properties')
        for p in self.properties:
            location = self.th.create_property('properties', p)
            mapped_uris = self.uf.do_link_canonical_property_to_local(p, location, 'trellis')
            self.public_uris['properties'][mapped_uris['canonicalURILanguageStr']] = mapped_uris['localUri']
            self.private_uris['properties'][mapped_uris['localUri']] = mapped_uris['canonicalURILanguageStr']

    def __insert_all_entities(self):
        for c in self.classes:
            location = self.th.create_basic_container(None,c)
            mapped_uris = self.uf.do_link_canonical_entity_to_local(c, location, 'trellis')
            self.public_uris['entities'][mapped_uris['canonicalURILanguageStr']] = mapped_uris['localUri']
            self.private_uris['entities'][mapped_uris['localUri']] = mapped_uris['canonicalURILanguageStr']

    def __insert_all_instances(self):
        for inst in self.instances:
            location = self.th.create_instance(inst,self.instancesMap)
            mapped_uris = self.uf.do_link_canonical_instance_to_local(inst, location, 'trellis')
            self.public_uris['instances'][mapped_uris['canonicalURILanguageStr']] = mapped_uris['localUri']
            self.private_uris['instances'][mapped_uris['localUri']] = mapped_uris['canonicalURILanguageStr']

    def get_properties(self):
        return self.properties

    def get_instances(self):
        return self.instances

    def get_instances_map(self):
        return self.instancesMap