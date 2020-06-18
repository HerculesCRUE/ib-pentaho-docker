class FairEvaluator:
    def __init__(self,trellis_handler,uris_factory_handler,uris_list):
        self.uris_list = uris_list
        self.th = trellis_handler
        self.uf = uris_factory_handler