class Instance:
    def __init__(self,index, jsonObj, parent):
        self.id = index
        self.className = jsonObj['class']
        self.properties = {}
        self.childInstances = []
        self.canonicalURIS = {}
        for p in jsonObj['properties']:
            self.properties[p] = "%s_%s" % (p,index)
        if parent is not None:
            if jsonObj['parentProperty'] is not None:
                if jsonObj['parentProperty'] not in parent.properties:
                    parent.properties[jsonObj['parentProperty']] = []
                parent.properties[jsonObj['parentProperty']].append(self.id)
            self.properties[jsonObj['childProperty']] = parent.id

    def add_child(self,child):
        self.childInstances.append(child)

    def set_canonical_uris(self, canonical_uris_obj):
        self.canonicalURIS = canonical_uris_obj
        self.properties['has-canonical-uri'] = self.canonicalURIS['canonicalLanguageURI']

    def get_properties(self):
        return list(self.properties.keys())

    def get_instance_json_object(self):
        obj = {
            '@class': self.className
        }
        for key in self.properties:
            obj[key] = self.properties[key]
        return obj

    def generate_turtle_rdf(self, instaces_map):
        rdf =  "@prefix dc: <http://purl.org/dc/terms/>.\n"
        rdf += "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.\n"
        rdf += "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.\n"
        rdf += "@prefix p: <http://hercules.org/um/en-EN/res/>.\n"
        rdf += "\n"
        rdf += "<>\n"
        rdf += "    a rdfs:Resource ;"
        # rdf += "    p:name 'name';"
        rdf += "    dc:title 'Instance %s of class %s';" % (self.id,self.className)
        for p in self.properties:
            if type(self.properties[p]) is not list:
                rdf += ";\n\tp:%s '%s'" % (p,self.properties[p])
            else:
                for p_in in self.properties[p]:
                    uri = instaces_map[p_in].canonicalURIS['canonicalLanguageURI']
                    rdf += ";\n\tp:%s '%s'" % (p, uri)
        rdf += "."
        return rdf

    def __str__(self):
        return "%s:%s" % (self.className,self.id)
