from DivvyPlugins.hookpoints import hookpoint
from elasticsearch import Elasticsearch
import logging
logger = logging.getLogger("ElasticSearch_Plugin")
from DivvyInterfaceMessages import ResourceConverter
import simplejson as json
fh = None


elastic_server = None

def load():
	global elastic_server
	global fh
	elastic_server = '54.174.215.250:9200'
	fh = logging.FileHandler('logs/elasticsearch.log')
	fh.setLevel(logging.DEBUG)
	logger.addHandler(fh)

def unload():
	global elastic_server
	global fh
	elastic_server = None
	logger.removeHandler(fh)

@hookpoint('divvycloud.instance.modified')
def instance_modified(resource, old_resource=None, user_resource_id=None):
	global elastic_server
	logger.info("Instance Modified .. adding to ES")
	try:
		es = Elasticsearch(elastic_server)
		converted_resource = ResourceConverter.converted_resource(resource)
		data = json.dumps(converted_resource)
		logger.debug(data)
		es.index(index="instances",doc_type="JSON",id=resource.resource_id,body=data)
	except Exception,e:
		logger.info(e)




@hookpoint('divvycloud.instance.created')
def instance_created(resource, user_resource_id=None):
	global elastic_server
	logger.info("Instance Created.. adding to ES")
	try:
		es = Elasticsearch(elastic_server)
		converted_resource = ResourceConverter.converted_resource(resource)
		data = json.dumps(converted_resource)
		logger.debug(data)
		es.index(index="instances",doc_type="JSON",id=resource.resource_id,body=data)
	except Exception,e:
		logger.info(e)

