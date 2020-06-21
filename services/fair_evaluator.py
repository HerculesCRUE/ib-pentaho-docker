import json
from rdflib.graph import Graph
import pandas as pd
from models.instance import Instance

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class FairEvaluator:
    def __init__(self,trellis_handler,uris_factory_handler):
        # with open('./data/public_uris.json','r') as f:
        #     self.uris_list = json.loads(f.read())
        # with open('./data/private_uris.json','r') as f:
        #     self.uris_list_privates = json.loads(f.read())
        # self.th = trellis_handler
        # self.uf = uris_factory_handler
        self.th = trellis_handler
        self.uf = uris_factory_handler
        self.uris_list, self.uris_list_privates = self.__pupulate_uris()
        self.values = {
            '0': 'not applicable',
            '1': 'not being considered this yet',
            '2': 'under consideration or in planning phase',
            '3': 'in implementation phase',
            '4': 'fully implemented'
        }
        self.uris_metadata_ids,self.uris_metadata,self.uris_metadata_headers = self.__populate_metadata_ids_from_uri_list()
        self.uris_mementos_metadata_ids,self.uri_mementos_metadata,self.uris_mementos_metadata_headers  = self.__populate_metadata_mementos_ids_from_uri_list()
        self.uris_data_ids = self.__populate_data_ids_from_uri_list()
        self.headers, self.triples = self.__populate_responses_from_uri_list()
        self.evaluation = pd.read_csv("./data/FAIR_evaluation.csv")
        print('Generated file '+bcolors.BOLD+'FAIR_evaluation_out.csv with the metrics evaluation results'+bcolors.ENDC)

    def evaluate_fair(self):
        self.evaluate_findable()
        self.evaluate_accessible()
        self.evaluate_interoperable()
        self.evaluate_reusable()
        print(self.evaluation)
        self.evaluation.to_csv("./data/FAIR_evaluation_out.csv")

    def evaluate_findable(self):
        print('\n'+'::' * 50)
        print('Evaluating findable metrics...')
        self.evaluate_RDA_F1_01M()
        self.evaluate_RDA_F1_01D()
        self.evaluate_RDA_F1_02M()
        self.evaluate_RDA_F1_02D()
        self.evaluate_RDA_F2_01M()
        self.evaluate_RDA_F3_01M()
        print('\t'+'-'*96)
        print('::' * 50)


    ######################## FINDABLES #######################################################################
    def evaluate_findable(self):
        print('\n'+'::' * 50)
        print('Evaluating findable metrics...')
        self.evaluate_RDA_F1_01M()
        self.evaluate_RDA_F1_01D()
        self.evaluate_RDA_F1_02M()
        self.evaluate_RDA_F1_02D()
        self.evaluate_RDA_F2_01M()
        self.evaluate_RDA_F3_01M()
        print('\t'+'-'*96)
        print('::' * 50)

    def evaluate_RDA_F1_01M(self):
        indicator_id = 'RDA-F1-01M'
        hits = 0
        fails = 0
        for t in self.uris_metadata_ids:
            for uri in self.uris_metadata_ids[t]:
                if len(self.uris_metadata_ids[t][uri])>0:
                    hits += 1
                else:
                    fails += 1
        result = self.__get_evaluation(hits,fails)
        self.print_leyend('F1', indicator_id, 'Essential', 'Metadata is identified by a persistent identifier', self.values[str(result)])
        self.__update_metric_with_result(indicator_id, result)


    def evaluate_RDA_F1_01D(self):
        indicator_id = 'RDA-F1-01D'
        hits = 0
        fails = 0
        for t in self.uris_data_ids:
            for uri in self.uris_data_ids[t]:
                if len(self.uris_data_ids[t][uri]) > 0:
                    hits += 1
                else:
                    fails += 1
        result = self.__get_evaluation(hits, fails)
        self.print_leyend('F1', indicator_id, 'Essential', 'Data is identified by a persistent identifier',self.values[str(result)])
        self.__update_metric_with_result(indicator_id, result)

    def evaluate_RDA_F1_02M(self):
        indicator_id = 'RDA-F1-02M'
        hits = 0
        fails = 0
        ids = set()
        for t in self.uris_metadata_ids:
            for uri in self.uris_metadata_ids[t]:
                for metadata_id in self.uris_metadata_ids[t][uri]:
                    if metadata_id not in ids:
                        hits += 1
                        ids.add(metadata_id)
                    else:
                        fails += 1
        result = self.__get_evaluation(hits, fails)
        self.print_leyend('F1', indicator_id, 'Essential', 'Metadata is identified by a globally unique identifier',
                          self.values[str(result)])
        self.__update_metric_with_result(indicator_id, result)

    def evaluate_RDA_F1_02D(self):
        indicator_id = 'RDA-F1-02D'
        hits = 0
        fails = 0
        ids = set()
        for t in self.uris_data_ids:
            for uri in self.uris_data_ids[t]:
                if uri not in ids:
                    hits += 1
                    ids.add(uri)
                else:
                    fails += 1
        result = self.__get_evaluation(hits, fails)
        self.print_leyend('F1', indicator_id, 'Essential', 'Data is identified by a globally unique identifier',
                          self.values[str(result)])
        self.__update_metric_with_result(indicator_id, result)

    def evaluate_RDA_F2_01M(self):
        indicator_id = 'RDA-F2-01M'
        hits = 0
        fails = 0
        ids = set()
        # Has headers to link with resources
        for uri in self.headers['entities']:
            if 'link' in self.headers['entities'][uri] and len(self.headers['entities'][uri]['link'].split(','))>0:
                hits += 1
            else:
                fails += 1
         # Container has triples for content
        for uri in self.triples['entities']:
            contains = 0
            for triple in self.triples['entities'][uri]:
                if '<http://www.w3.org/ns/ldp#contains>' in triple[0]:
                    contains += 1
            if contains>0:
                hits += 1
            else:
                fails += 1
        result = self.__get_evaluation(hits, fails)
        self.print_leyend('F2', indicator_id, 'Essential', 'Rich metadata is provided to allow discovery',
                          self.values[str(result)])
        self.__update_metric_with_result(indicator_id, result)

    def evaluate_RDA_F3_01M(self):
        indicator_id = 'RDA-F3-01M'
        hits = 0
        fails = 0
        ids = set()
        # Has headers to link with resources
        for t in self.uri_mementos_metadata:
            for uri in self.uri_mementos_metadata[t]:
                found = False
                for inner_uri in self.uri_mementos_metadata[t][uri]:
                    if uri in inner_uri:
                        found = True
                        break
                if found:
                    hits += 1
                else:
                    fails += 1
        result = self.__get_evaluation(hits, fails)
        self.print_leyend('F3', indicator_id, 'Essential', 'Metadata includes the identifier for the data',
                          self.values[str(result)])
        self.__update_metric_with_result(indicator_id, result)

    ######################## ACCESSIBLE #######################################################################

    def evaluate_accessible(self):
        print('\n' + '::' * 50)
        print('Evaluating accessible metrics...')
        self.evaluate_RDA_A1_01M()
        self.evaluate_RDA_A1_03M()
        self.evaluate_RDA_A1_03D()
        self.evaluate_RDA_A1_04M_and_RDA_A1_1_01M()
        self.evaluate_RDA_A1_04D_and_RDA_A1_1_01D_and_RDA_A1_1_02D()
        self.evaluate_RDA_A1_05D()
        self.evaluate_RDA_A2_01M()
        print('\t' + '-' * 96)
        print('::' * 50)

    def evaluate_RDA_A1_01M(self):
        indicator_id = 'RDA-A1-01M'
        hits = 0
        fails = 0
        ids = set()
        # Has headers to link with resources
        for t in self.uri_mementos_metadata:
            for uri in self.uri_mementos_metadata[t]:
                found = False
                for inner_uri in self.uri_mementos_metadata[t][uri]:
                    if uri in inner_uri:
                        found = True
                        break
                if found:
                    hits += 1
                else:
                    fails += 1
        result = self.__get_evaluation(hits, fails)
        self.print_leyend('A1', indicator_id, 'Important','Metadata contains information to enable the user to get access to the data',
                          self.values[str(result)])
        self.__update_metric_with_result(indicator_id, result)

    def evaluate_RDA_A1_03M(self):
        indicator_id = 'RDA-A1-03M'
        hits = 0
        fails = 0
        ids = set()
        # Has headers to link with resources
        for t in self.uri_mementos_metadata:
            for uri in self.uri_mementos_metadata[t]:
                if len(self.uri_mementos_metadata[t][uri])>0:
                    hits += 1
                else:
                    fails += 1
        result = self.__get_evaluation(hits, fails)
        self.print_leyend('A1', indicator_id, 'Important','Metadata identifier resolves to a metadata record',
                          self.values[str(result)])
        self.__update_metric_with_result(indicator_id, result)

    def evaluate_RDA_A1_03D(self):
        indicator_id = 'RDA-A1-03D'
        hits = 0
        fails = 0
        ids = set()
        # Has headers to link with resources
        for t in self.triples:
            for uri in self.triples[t]:
                if len(self.triples[t][uri])>0:
                    hits += 1
                else:
                    fails += 1
        result = self.__get_evaluation(hits, fails)
        self.print_leyend('A1', indicator_id, 'Important','Data identifier resolves to a digital object',
                          self.values[str(result)])
        self.__update_metric_with_result(indicator_id, result)

    def evaluate_RDA_A1_04M_and_RDA_A1_1_01M(self):
        indicator_id1 = 'RDA-A1-04M'
        indicator_id2 = 'RDA-A1.1-01M'
        hits = 0
        fails = 0
        ids = set()
        # Has headers to link with resources
        for t in self.uris_list:
            for uri in self.uris_list[t]:
                if 'http://' in (self.uris_list[t][uri]+'?ext=timemap'):
                    hits += 1
                else:
                    fails +=1
        result = self.__get_evaluation(hits, fails)
        self.print_leyend('A1', indicator_id1, 'Important','Metadata is accessed through standardised protocol',
                          self.values[str(result)])
        self.print_leyend('A1.1', indicator_id2, 'Important', 'Metadata is accessible through a free access protocol',
                          self.values[str(result)])
        self.__update_metric_with_result(indicator_id1, result)
        self.__update_metric_with_result(indicator_id2, result)

    def evaluate_RDA_A1_04D_and_RDA_A1_1_01D_and_RDA_A1_1_02D(self):
        indicator_id = 'RDA-A1-04D'
        indicator_id2 = 'RDA-A1.1-01D'
        indicator_id3 = 'RDA-A1.2-02D'
        hits = 0
        fails = 0
        # Has headers to link with resources
        for t in self.uris_list:
            for uri in self.uris_list[t]:
                if 'http://' in self.uris_list[t][uri]:
                    hits += 1
                else:
                    fails +=1
        result = self.__get_evaluation(hits, fails)
        self.print_leyend('A1', indicator_id, 'Important','Data is accessible through standardised protocol',
                          self.values[str(result)])
        self.print_leyend('A1.1', indicator_id2, 'Important','Data is accessible through a free access protocol',
                          self.values[str(result)])
        self.print_leyend('A1.2', indicator_id3, 'Important','Data is accessible through an access protocol that supports authentication and authorisation',
                          self.values[str(result)])
        self.__update_metric_with_result(indicator_id, result)
        self.__update_metric_with_result(indicator_id2, result)
        self.__update_metric_with_result(indicator_id3, result)

    def evaluate_RDA_A1_05D(self):
        indicator_id = 'RDA-A1-05D'
        hits = 0
        fails = 0
        ids = set()
        # Has headers to link with resources
        for t in self.triples:
            for uri in self.triples[t]:
                if len(self.triples[t][uri])>0:
                    hits += 1
                else:
                    fails += 1
        result = self.__get_evaluation(hits, fails)
        self.print_leyend('A1', indicator_id, 'Important','Data can be accessed automatically (i.e. by a computer program)',
                          self.values[str(result)])
        self.__update_metric_with_result(indicator_id, result)

    def evaluate_RDA_A2_01M(self):
        indicator_id = 'RDA-A2-01M'
        hits = 0
        fails = 0

        # Delete container
        self.th.delete_resource('http://localhost:8080/test1')
        # Create container
        trellis_location = self.th.create_basic_container(None, 'test1')
        # Create canonical uri

        canonical = self.uf.create_canonical_entity('test')
        uris_link_before = self.uf.do_link_canonical_entity_to_local('test',trellis_location,'trellis')
        result = self.__get_evaluation(hits, fails)

        # Delete container
        self.th.delete_resource('http://localhost:8080/test1')
        self.th.delete_resource('http://localhost:8080/test2')
        # Create container
        trellis_location_2 = self.th.create_basic_container(None, 'test2')
        # Delete link
        self.uf.do_unlink_canonical_entity_to_local('test',trellis_location,'trellis')
        uris_link_after = self.uf.do_link_canonical_entity_to_local('test', trellis_location_2, 'trellis')

        if uris_link_after['localUri'] == trellis_location_2:
            hits +=1
        else:
            fails += 1
        result = self.__get_evaluation(hits, fails)
        self.print_leyend('A2', indicator_id,'Essential', 'Metadata is guaranteed to remain available after data is no longer available',
                          self.values[str(result)])
        self.__update_metric_with_result(indicator_id, result)


    ######################## INTEROPERABLE #######################################################################

    def evaluate_interoperable(self):
        print('\n' + '::' * 50)
        print('Evaluating interoperable metrics...')
        self.evaluate_RDA_I1_01M_and_RDA_I1_02M()
        self.evaluate_RDA_I1_01D_and_RDA_I1_02D()
        self.evaluate_RDA_I3_01M()
        self.evaluate_RDA_I3_01D()
        print('\t' + '-' * 96)
        print('::' * 50)


    def evaluate_RDA_I1_01M_and_RDA_I1_02M(self):
        indicator_id_1 = 'RDA-I1-01M'
        indicator_id_2 = 'RDA-I1-02M'
        hits = 0
        fails = 0
        ids = set()
        # Has headers to link with resources
        for t in self.uris_metadata_headers:
            for uri in self.uris_metadata_headers[t]:
                if 'text/turtle' in self.uris_metadata_headers[t][uri]['content-type']:
                    hits += 1
                else:
                    fails += 1
        result = self.__get_evaluation(hits, fails)
        self.print_leyend('I1', indicator_id_1, 'Important','Metadata uses knowledge representation expressed in standardised format',
                          self.values[str(result)])
        self.__update_metric_with_result(indicator_id_1, result)
        self.print_leyend('I1', indicator_id_2, 'Important',
                          'Metadata uses machine-understandable knowledge representation',
                          self.values[str(result)])
        self.__update_metric_with_result(indicator_id_2, result)

    def evaluate_RDA_I1_01D_and_RDA_I1_02D(self):
        indicator_id_1 = 'RDA-I1-01D'
        indicator_id_2 = 'RDA-I1-02D'
        hits = 0
        fails = 0
        ids = set()
        # Has headers to link with resources
        for t in self.headers:
            for uri in self.headers[t]:
                if 'text/turtle' in self.headers[t][uri]['content-type']:
                    hits += 1
                else:
                    fails += 1
        result = self.__get_evaluation(hits, fails)
        self.print_leyend('I1', indicator_id_1, 'Important','Data uses knowledge representation expressed in standardised format',
                          self.values[str(result)])
        self.__update_metric_with_result(indicator_id_1, result)
        self.print_leyend('I1', indicator_id_2, 'Important',
                          'Data uses machine-understandable knowledge representation',
                          self.values[str(result)])
        self.__update_metric_with_result(indicator_id_2, result)

    def evaluate_RDA_I3_01M(self):
        indicator_id_1 = 'RDA-I3-01M'
        hits = 0
        fails = 0
        ids = set()
        # Has headers to link with resources
        for t in self.headers:
            for uri in self.headers[t]:
                if len(self.headers[t][uri]['link'])>0:
                    hits += 1
                else:
                    fails += 1
        result = self.__get_evaluation(hits, fails)
        self.print_leyend('I3', indicator_id_1, 'Important','Metadata includes references to other metadata',
                          self.values[str(result)])
        self.__update_metric_with_result(indicator_id_1, result)

    def evaluate_RDA_I3_01D(self):
        indicator_id_1 = 'RDA-I3-01D'
        hits = 0
        fails = 0
        ids = set()
        # Has headers to link with resources
        for uri in self.triples['entities']:
            contains = 0
            for triple in self.triples['entities'][uri]:
                if 'contains' in triple[0]:
                    t0 = triple[0]
                    t1 = triple[1][1:-1]
                    if triple[1][1:-1] in self.uris_list_privates['instances']:
                        hits += 1
                    else:
                        fails += 1
        result = self.__get_evaluation(hits, fails)
        self.print_leyend('I1', indicator_id_1, 'Essential','Data includes references to other data',
                          self.values[str(result)])
        self.__update_metric_with_result(indicator_id_1, result)


    ######################## REUSABLE #######################################################################

    def evaluate_reusable(self):
        print('\n' + '::' * 50)
        print('Evaluating reusable metrics...')
        self.evaluate_RDA_R1_01M()
        self.evaluate_RDA_R1_2_01M_and_RDA_R1_2_02M()
        self.evaluate_RDA_R1_3_01M_and_RDA_R1_3_02M()
        self.evaluate_RDA_R1_3_01D_and_RDA_R1_3_02D()
        print('\t' + '-' * 96)
        print('::' * 50)


    def evaluate_RDA_R1_01M(self):
        indicator_id_1 = 'RDA-R1-01M'
        hits = 0
        fails = 0
        ids = set()
        # Has headers to link with resources

        for uri in self.triples['instances']:
            properties = 0
            no_properties = 0
            for triple in self.triples['instances'][uri]:
                if 'http://localhost/properties' in triple[0]:
                    properties += 1
                elif 'http://':
                    properties += 1
                else:
                    no_properties += 1
            if properties>0 and no_properties ==0:
                hits += 1
            else:
                fails += 1
        result = self.__get_evaluation(hits, fails)
        self.print_leyend('R1', indicator_id_1, 'Essential', 'Plurality of accurate and relevant attributes are provided to allow reuse',
                          self.values[str(result)])
        self.__update_metric_with_result(indicator_id_1, result)

    def evaluate_RDA_R1_2_01M_and_RDA_R1_2_02M(self):
        indicator_id_1 = 'RDA-R1.2-01M'
        indicator_id_2 = 'RDA-R1.2-02M'
        hits1 = 0
        fails1 = 0
        hits2 = 0
        fails2 = 0
        # Has headers to link with resources

        for t in self.uris_metadata:
            for uri in self.uris_metadata[t]:
                id_metadata = None
                found_prov = False
                for triples_uri in self.uris_metadata[t][uri]['<'+uri+'>']:
                    if triples_uri[0] == '<http://www.w3.org/ns/prov#wasGeneratedBy>':
                        id_metadata = triples_uri[1]
                        found_prov = True
                if id_metadata is None:
                    for triples_uri in self.uris_metadata[t][uri]['<' + uri[:-1] + '>']:
                        if triples_uri[0] == '<http://www.w3.org/ns/prov#wasGeneratedBy>':
                            id_metadata = triples_uri[1]
                            found_prov = True
                if id_metadata is not None and len(self.uris_metadata[t][uri][id_metadata])>0:
                    hits1 += 1
                else:
                    fails1 += 1
                if found_prov:
                    hits2 += 1
                else:
                    fails2 += 1
        result1 = self.__get_evaluation(hits1, fails1)
        self.print_leyend('R1.2', indicator_id_1, 'Essential', 'Metadata includes provenance information according to community-specific standards',
                          self.values[str(result1)])
        self.__update_metric_with_result(indicator_id_1, result1)

        result2 = self.__get_evaluation(hits2, fails2)
        self.print_leyend('R1.2', indicator_id_2, 'Essential', 'Metadata includes provenance information according to a cross-community language',
                          self.values[str(result2)])
        self.__update_metric_with_result(indicator_id_2, result2)


    def evaluate_RDA_R1_3_01M_and_RDA_R1_3_02M(self):
        indicator_id_1 = 'RDA-R1.3-01M'
        indicator_id_2 = 'RDA-R1.3-02M'
        hits = 0
        falis = 0
        # Has headers to link with resources

        for t in self.uris_metadata:
            for uri in self.uris_metadata[t]:
                common_ontologies = 0
                for subject in self.uris_metadata[t][uri]:
                    for triples in self.uris_metadata[t][uri][subject]:
                        if 'http://purl.org/dc/terms' in triples[0]  or \
                            'http://www.w3.org/1999/02/22-rdf-syntax-ns'  in triples[0]  or \
                            'http://www.w3.org/ns/ldp#contains'  in triples[0]  or \
                            'http://www.w3.org/ns/prov' in triples[0]:
                            common_ontologies +=1
                if common_ontologies>0:
                    hits += 1
                else:
                    falis += 1
        result = self.__get_evaluation(hits, falis)
        self.print_leyend('R1.3', indicator_id_1, 'Essential', 'Metadata complies with a community standard',
                          self.values[str(result)])
        self.__update_metric_with_result(indicator_id_1, result)

        self.print_leyend('R1.3', indicator_id_2, 'Essential', 'Metadata is expressed in compliance with a machine-understandable community standard',
                          self.values[str(result)])
        self.__update_metric_with_result(indicator_id_2, result)


    def evaluate_RDA_R1_3_01D_and_RDA_R1_3_02D(self):
        indicator_id_1 = 'RDA-R1.3-01D'
        indicator_id_2 = 'RDA-R1.3-02D'
        hits = 0
        falis = 0
        # Has headers to link with resources

        for t in self.uris_metadata:
            for uri in self.triples[t]:
                common_ontologies = 0
                for triples in self.triples[t][uri]:
                    for triple in triples:
                        if 'http://purl.org/dc/terms' in triple  or \
                            'http://www.w3.org/1999/02/22-rdf-syntax-ns'  in triple  or \
                            'http://www.w3.org/ns/ldp#contains'  in triple  or \
                            'http://www.w3.org/ns/prov' in triple:
                            common_ontologies +=1
                if common_ontologies>0:
                    hits += 1
                else:
                    falis += 1
        result = self.__get_evaluation(hits, falis)
        self.print_leyend('R1.3', indicator_id_1, 'Essential', 'Data complies with a community standard',
                          self.values[str(result)])
        self.__update_metric_with_result(indicator_id_1, result)

        self.print_leyend('R1.3', indicator_id_2, 'Essential', 'Data is expressed in compliance with a machine-understandable community standard',
                          self.values[str(result)])
        self.__update_metric_with_result(indicator_id_2, result)

    ####################### Private Fucntions

    def serialize_turtle(self, rdf):
        triples = {};
        g1 = Graph().parse(format='turtle', data=rdf)
        for l in sorted(g1.serialize(format='nt').splitlines()):
            if l:
                line = l.decode('ascii').split(' ')[0:-1]
                if line[0] not in triples:
                    triples[line[0]] = []
                triples[line[0]].append(line[1:])
        return triples

    def print_leyend(self,principle, indicator_id, type, description, result):
        print('\t'+'-'*96)
        print('\t'+bcolors.WARNING+'Principle: '+principle+bcolors.ENDC)
        print('\tIndicator: %s' % indicator_id)
        print('\tLevel: %s' % type)
        print('\tDescription: %s' % description)
        if result == 'fully implemented':
            print('\t'+bcolors.OKGREEN +'Evaluation Result: ' + result +bcolors.ENDC)
        else:
            print('\t' + bcolors.FAIL + 'Evaluation Result: ' + result + bcolors.ENDC)

    def __update_metric_with_result(self, indicator,result):
        self.evaluation.loc[self.evaluation['INDICATOR_ID'] == indicator, ['METRIC','SCORE','MANUAL']] = result,1 if result == 4 else 0,0

    def __populate_metadata_ids_from_uri_list(self):
        metadata_uris_list = {}
        metadata_uris_data_list = {}
        metadata_uris_headers_list = {}
        for t in self.uris_list:
            if t not in metadata_uris_list:
                metadata_uris_list[t] = {}
                metadata_uris_data_list[t] = {}
                metadata_uris_headers_list[t] = {}
            for uri in self.uris_list[t]:
                resource_uri = self.uris_list[t][uri]
                resource_uris = [resource_uri]
                if resource_uri[-1] == '/':
                    resource_uris.append(resource_uri[:-1])
                h,b = self.th.get_audit_metadata(resource_uri)
                triples = self.serialize_turtle(b)
                l = self.__get_metadata_id(triples,resource_uris)
                metadata_uris_list[t][resource_uri] = l
                metadata_uris_headers_list[t][resource_uri] = h
                if '<' + resource_uri + '>' in triples:
                    metadata_uris_data_list[t][resource_uri] = triples
        return metadata_uris_list,metadata_uris_data_list,metadata_uris_headers_list

    def __populate_metadata_mementos_ids_from_uri_list(self):
        metadata_uris_list = {}
        metadata_uris_data_list = {}
        metadata_uris_headers_list = {}
        for t in self.uris_list:
            if t not in metadata_uris_list:
                metadata_uris_list[t] = {}
                metadata_uris_data_list[t] = {}
                metadata_uris_headers_list[t] = {}
            for uri in self.uris_list[t]:
                resource_uri = self.uris_list[t][uri]
                resource_uris = [resource_uri]
                if resource_uri[-1] == '/':
                    resource_uris.append(resource_uri[:-1])
                h,b = self.th.get_mementos_metadata(resource_uri)
                triples = self.serialize_turtle(b)
                l = self.__get_metadata_id(triples,resource_uris)
                metadata_uris_list[t][resource_uri] = l
                metadata_uris_headers_list[t][resource_uri] = h
                if '<' + resource_uri + '>' in triples:
                    metadata_uris_data_list[t][resource_uri] = triples
        return metadata_uris_list,metadata_uris_data_list,metadata_uris_headers_list

    def __populate_data_ids_from_uri_list(self):
        data_uris_list = {}
        for t in self.uris_list:
            if t not in data_uris_list:
                data_uris_list[t] = {}
            for uri in self.uris_list[t]:
                resource_uri = self.uris_list[t][uri]
                h, b = self.th.get_data(resource_uri)
                triples = self.serialize_turtle(b)
                l = self.__get_data_id(triples, [resource_uri])
                data_uris_list[t][resource_uri] = l
        return data_uris_list

    def __populate_responses_from_uri_list(self):
        resources_uris_list = {}
        headers_uris_list = {}
        for t in self.uris_list:
            if t not in resources_uris_list:
                resources_uris_list[t] = {}
                headers_uris_list[t] = {}
            for uri in self.uris_list[t]:
                resource_uri = self.uris_list[t][uri]
                h, b = self.th.get_data(resource_uri)
                headers_uris_list[t][resource_uri] = h
                triples = self.serialize_turtle(b)
                if '<'+resource_uri+'>' in triples:
                    resources_uris_list[t][resource_uri] = triples['<'+resource_uri+'>']
        return headers_uris_list,resources_uris_list

    def __get_evaluation(self,hints, fails):
        if fails == 0:
            return 4
        if hints > fails:
            return 3
        if hints == 0:
            return 2
        else:
            return 1


    def __get_metadata_id(self,triples,resource_ids):
        metadata_keys = []
        for resource_id in resource_ids:
            resource_key = '<'+resource_id+'>'
            if resource_key in triples:
                for tripe in triples[resource_key]:
                    if '_:' in tripe[1]:
                        metadata_keys.append(tripe[1])
        return metadata_keys

    def __get_data_id(self,triples,resource_ids):
        data_keys = []
        for resource_id in resource_ids:
            resource_key = '<'+resource_id+'>'
            if resource_key in triples:
                for tripe in triples[resource_key]:
                    if '_:' not in tripe[1]:
                        data_keys.append(tripe[1])
        return data_keys

    def __pupulate_uris(self):
        public = {
            'properties': {},
            'entities': {},
            'instances':{}
        }
        privates = {
            'properties': {},
            'entities': {},
            'instances': {}
        }

        for canonical in self.uf.get_all_canonical_uri_language():
            canonical_full_uri = canonical['fullURI'];
            local_uris = self.uf.get_local_storage_by_canonical_uri(
                canonical['fullURI'], 'en-EN', 'trellis')
            try:
                local_uri = local_uris[0]
                if canonical['isEntity']:
                    public['entities'][canonical_full_uri] = local_uri['localUri']
                    privates['entities'][local_uri['localUri']] = canonical_full_uri
                elif canonical['isProperty']:
                    public['properties'][canonical_full_uri] = local_uri['localUri']
                    privates['properties'][local_uri['localUri']] = canonical_full_uri
                else:
                    public['instances'][canonical_full_uri] = local_uri['localUri']
                    privates['instances'][local_uri['localUri']] = canonical_full_uri
            except:
                pass

        return public,privates