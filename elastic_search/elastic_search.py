from DivvyPlugins.hookpoints import hookpoint
from elasticsearch import Elasticsearch
import logging
logger = logging.getLogger("ElasticSearch_Plugin")
from DivvyInterfaceMessages.ResourceConverters import convert_resource
import simplejson as json
from datetime import datetime
fh = None
elastic_server = None

def load():
    global elastic_server
    global fh
    elastic_server = '54.174.215.250:5601'
    fh = logging.FileHandler('elasticsearch.log')
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    logger.info("Loaded")

def unload():
    global elastic_server
    global fh
    elastic_server = None
    logger.removeHandler(fh)

@hookpoint('divvycloud.instance.modified')
def instance_modified(resource, old_resource=None, user_resource_id=None):
    global elastic_server
    global logger
    logger.info("Using [%s]" % (elastic_server))
    try:
        logger.info("Insatnces [%s] was modified" % (resource.resource_id))
        es = Elasticsearch(elastic_server)
        converted_resource = convert_resource(resource)
        converted_resource.event_time = datetime.utcnow().isoformat()
        data = json.dumps(converted_resource)
        es.index(index="instances",doc_type="JSON",id=resource.resource_id,body=data)
    except Exception,e:
        logger.info(e)


@hookpoint('divvycloud.instance.created')
def instance_created(resource, user_resource_id=None):
    global elastic_server
    global logger
    logger.info("Insatnces [%s] was created" % (resource.resource_id))
    try:
        es = Elasticsearch(elastic_server)
        converted_resource = convert_resource(resource)
        data = json.dumps(converted_resource)
        es.index(index="instances",doc_type="JSON",id=resource.resource_id,body=data)
    except Exception,e:
        logger.info(e)


@hookpoint('divvycloud.instance.destroyed')
def instance_destroyed(resource, user_resource_id=None):
    global elastic_server
    global logger
    logger.info("Insatnces [%s] was destroyed" % (resource.resource_id))
    try:
        es = Elasticsearch(elastic_server)
        converted_resource = convert_resource(resource)
        converted_resource.event_time = datetime.utcnow().isoformat()
        data = json.dumps(converted_resource)
        es.index(index="instances",doc_type="JSON",id=resource.resource_id,body=data)
    except Exception,e:
        logger.info(e)



