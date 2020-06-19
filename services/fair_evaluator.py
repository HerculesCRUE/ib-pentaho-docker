import json
from rdflib.graph import Graph
import pandas as pd

class FairEvaluator:
    def __init__(self,trellis_handler,uris_factory_handler):
        with open('./data/public_uris.json','r') as f:
            self.uris_list = json.loads(f.read())
        self.th = trellis_handler
        self.uf = uris_factory_handler
        self.values = {
            '0': 'not applicable',
            '1': 'not being considered this yet',
            '2': 'under consideration or in planning phase',
            '3': 'in implementation phase',
            '4': 'fully implemented'
        }
        self.uris_metadata_ids,self.uris_metadata = self.__populate_metadata_ids_from_uri_list()
        self.uris_data_ids = self.__populate_data_ids_from_uri_list()
        self.headers, self.triples = self.__populate_responses_from_uri_list()
        self.evaluation = pd.read_csv("./data/FAIR_evaluation.csv")

    def evaluate_fair(self):
        self.evaluate_findable()

        print(self.evaluation)

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
        self.print_leyend('F1',indicator_id,'Essential','Metadata is identified by a persistent identifier')
        hits = 0
        fails = 0
        for t in self.uris_metadata_ids:
            for uri in self.uris_metadata_ids[t]:
                if len(self.uris_metadata_ids[t][uri])>0:
                    hits += 1
                else:
                    fails += 1
        result = self.__get_evaluation(hits,fails)
        self.__update_metric_with_result(indicator_id, result)


    def evaluate_RDA_F1_01D(self):
        indicator_id = 'RDA-F1-01D'
        self.print_leyend('F1', indicator_id, 'Essential', 'Data is identified by a persistent identifier')
        hits = 0
        fails = 0
        for t in self.uris_data_ids:
            for uri in self.uris_data_ids[t]:
                if len(self.uris_data_ids[t][uri]) > 0:
                    hits += 1
                else:
                    fails += 1
        result = self.__get_evaluation(hits, fails)
        self.__update_metric_with_result(indicator_id, result)

    def evaluate_RDA_F1_02M(self):
        indicator_id = 'RDA-F1-02M'
        self.print_leyend('F1', indicator_id, 'Essential', 'Metadata is identified by a globally unique identifier')
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
        self.__update_metric_with_result(indicator_id, result)

    def evaluate_RDA_F1_02D(self):
        indicator_id = 'RDA-F1-02D'
        self.print_leyend('F1', indicator_id, 'Essential', 'Data is identified by a globally unique identifier')
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
        self.__update_metric_with_result(indicator_id, result)

    def evaluate_RDA_F2_01M(self):
        indicator_id = 'RDA-F2-01M'
        self.print_leyend('F2', indicator_id, 'Essential', 'Rich metadata is provided to allow discovery')
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
        self.__update_metric_with_result(indicator_id, result)

    def evaluate_RDA_F3_01M(self):
        indicator_id = 'RDA-F3-01M'
        self.print_leyend('F3', indicator_id, 'Essential', 'Metadata includes the identifier for the data')
        hits = 0
        fails = 0
        ids = set()
        # Has headers to link with resources
        for t in self.uris_metadata_ids:
            for uri in self.uris_metadata_ids[t]:
                if len(self.uris_metadata_ids[t][uri])>0:
                    hits += 1
                else:
                    fails += 1
        result = self.__get_evaluation(hits, fails)
        self.__update_metric_with_result(indicator_id, result)

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

    def print_leyend(self,principle, indicator_id, type, description):
        print('\t'+'-'*96)
        print('\tPrinciple: %s'%principle)
        print('\tIndicator: %s' % indicator_id)
        print('\tType: %s' % type)
        print('\tDescription: %s' % description)

    ####################### Private Fucntions

    def __update_metric_with_result(self, indicator,result):
        self.evaluation.loc[self.evaluation['INDICATOR_ID'] == indicator, ['METRIC','SCORE','MANUAL']] = result,1 if result == 4 else 0,0

    def __populate_metadata_ids_from_uri_list(self):
        metadata_uris_list = {}
        metadata_uris_data_list = {}
        for t in self.uris_list:
            if t not in metadata_uris_list:
                metadata_uris_list[t] = {}
                metadata_uris_data_list[t] = {}
            for uri in self.uris_list[t]:
                resource_uri = self.uris_list[t][uri]
                resource_uris = [resource_uri]
                if resource_uri[-1] == '/':
                    resource_uris.append(resource_uri[:-1])
                h,b = self.th.get_audit_metadata(resource_uri)
                triples = self.serialize_turtle(b)
                l = self.__get_metadata_id(triples,resource_uris)
                metadata_uris_list[t][resource_uri] = l
                if '<' + resource_uri + '>' in triples:
                    metadata_uris_data_list[t][resource_uri] = triples
        return metadata_uris_list,metadata_uris_data_list

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