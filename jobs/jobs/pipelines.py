# -*- coding: utf-8 -*-

import json
import hashlib
from elasticsearch import Elasticsearch

class JobsPipeline(object):
    def __init__(self):
        self.es = Elasticsearch()

    def process_item(self, item, spider):
        data = json.dumps(dict(item), ensure_ascii=False)
        hashcode = hashlib.md5(bytes(item["origin_url"], encoding="utf8")).hexdigest()
        
        results = self.es.index(index="jobs-index", doc_type="51job", id=hashcode, body=data)
        print("Done\t" + item["origin_url"])
