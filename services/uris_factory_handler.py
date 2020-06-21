import requests
import json

class URISFactoryHandler:
    def __init__(self, base, domain, sub_domain, language):
        self.uriFactoryBaseURL = base
        self.domain = domain
        self.sub_domain = sub_domain
        self.language = language

    def create_canonical_entity(self, entity):
        payload = {
            '@class': entity,
            'canonicalClassName': entity
        }
        params = {
            'domain': self.domain,
            'subDomain': self.sub_domain,
            'lang': self.language
        }
        headers = {
            'accept': '*/*',
            'Content-Type': 'application/json'
        }

        uri = self.uriFactoryBaseURL + 'uri-factory/canonical/entity'
        response = requests.request("POST", uri, headers=headers, params=params, data=json.dumps(payload))
        return json.loads(response.text.encode('utf8'))

    def create_canonical_instance(self, instance):
        payload = instance.get_instance_json_object()
        params = {
            'domain': self.domain,
            'subDomain': self.sub_domain,
            'lang': self.language
        }
        headers = {
            'accept': '*/*',
            'Content-Type': 'application/json'
        }
        uri = self.uriFactoryBaseURL + 'uri-factory/canonical/resource'
        response = requests.request("POST", uri, headers=headers, params=params, data=json.dumps(payload))

        #print(response.text.encode('utf8'))
        return json.loads(response.text.encode('utf8'))

    def create_canonical_property(self, property):
        payload = {
            'property': property,
            'canonicalProperty': property
        }
        params = {
            'domain': self.domain,
            'subDomain': self.sub_domain,
            'lang': self.language
        }
        headers = {
            'accept': '*/*',
            'Content-Type': 'application/json'
        }

        uri = self.uriFactoryBaseURL + 'uri-factory/canonical/property'
        response = requests.request("POST", uri, headers=headers, params=params, data=json.dumps(payload))
        return json.loads(response.text.encode('utf8'))

    def do_link_canonical_property_to_local(self, prop,local_uri,storage):
        params = {
            'domain': self.domain,
            'subDomain': self.sub_domain,
            'languageCode': self.language,
            'typeCode': 'res',
            'property': prop,
            'localURI': local_uri,
            'storageName': storage
        }
        headers = {
            'accept': '*/*',
            'Content-Type': 'application/json'
        }

        uri = self.uriFactoryBaseURL + 'uri-factory/local/property'
        response = requests.request("POST", uri, headers=headers, params=params)
        return json.loads(response.text.encode('utf8'))

    def do_link_canonical_entity_to_local(self, entity,local_uri,storage):
        params = {
            'domain': self.domain,
            'subDomain': self.sub_domain,
            'languageCode': self.language,
            'typeCode': 'res',
            'entity': entity,
            'localURI': local_uri,
            'storageName': storage
        }
        headers = {
            'accept': '*/*',
            'Content-Type': 'application/json'
        }

        uri = self.uriFactoryBaseURL + 'uri-factory/local/entity'
        response = requests.request("POST", uri, headers=headers, params=params)
        return json.loads(response.text.encode('utf8'))

    def do_unlink_canonical_entity_to_local(self, entity,local_uri,storage):
        params = {
            'domain': self.domain,
            'subDomain': self.sub_domain,
            'languageCode': self.language,
            'typeCode': 'res',
            'entity': entity,
            'localURI': local_uri,
            'storageName': storage
        }
        headers = {
            'accept': '*/*',
            'Content-Type': 'application/json'
        }

        uri = self.uriFactoryBaseURL + 'uri-factory/local/entity'
        response = requests.request("DELETE", uri, headers=headers, params=params)
        return response.status_code

    def do_link_canonical_instance_to_local(self, instance,local_uri,storage):
        canonical_id = instance.canonicalURIS['canonicalLanguageURI'].rsplit('/',1)[-1]
        params = {
            'domain': self.domain,
            'subDomain': self.sub_domain,
            'languageCode': self.language,
            'typeCode': 'res',
            'entity': instance.className,
            'reference': canonical_id,
            'localURI': local_uri,
            'storageName': storage
        }
        headers = {
            'accept': '*/*',
            'Content-Type': 'application/json'
        }

        uri = self.uriFactoryBaseURL + 'uri-factory/local/resource'
        response = requests.request("POST", uri, headers=headers, params=params)
        return json.loads(response.text.encode('utf8'))

    def get_all_canonical_uri_language(self):
        response = requests.request("GET",'http://localhost:9326/canonical-uri-language/all')
        return json.loads(response.text.encode('utf8'))

    def get_local_storage_by_canonical_uri(self,canonical_language_uri,language,storage):
        params = {
            'canonicalLanguageUri': canonical_language_uri,
            'languageCode': language,
            'languageCode': self.language,
            'storageName': storage
        }
        response = requests.request("GET", 'http://localhost:9326/uri-factory/local/canonical/language', params=params)
        return json.loads(response.text.encode('utf8'))