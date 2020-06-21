from services.scripts import BASH
from services.trellis_handler import TrellisHandler
from services.data_generator import DataGenerator
from services.uris_factory_handler import URISFactoryHandler
from services.fair_evaluator import FairEvaluator
import sys
import validators
import fairviz

def main():

    # print(validators.url('<http://hercules.org/um/en-EN/res/name>'.split('<')[1].split('>')[0]))
    uf = URISFactoryHandler('http://localhost:9326/', 'hercules.org', 'um', 'en-EN')
    th = TrellisHandler('localhost', '8080', None)
    if '-s' in sys.argv[1:] or '-S' in sys.argv[1:] :
        print('Building Sandbox')
        handle_deploy(20)
        print('Trellis deployed available in http://localhost:8080/')
        print('Fuseki deployed available in http://localhost:3030/')
        print('URIS Factory deployed\n\tSWAGGER available in http://localhost:9326/swagger-ui.htm\n\tAPI REST available in http://localhost:9326')

    if '-d' in sys.argv[1:] or '-D' in sys.argv[1:]:
        print('Building data....')
        dc = DataGenerator(open('./data/instances_generator_metadata.json'),th,uf)
        dc.generate_sintetic_data()

    if '-v' in sys.argv[1:] or '-V' in sys.argv[1:]:
        print('Build visualization....')
        fairviz.main()
    fe = FairEvaluator(th,uf)
    fe.evaluate_fair()

def handle_deploy(limit):
    bash = BASH()
    if not bash.start_environment(limit):
        handle_deploy(limit+5 if limit <=60 else limit)

if __name__ == '__main__':
    main()
