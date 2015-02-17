from DivvyPlugins.hookpoints import hookpoint
import logging
import simplejson as json
from DivvyResource.ResourceOperations import ResourceOperations_ResourceGroup


logger = logging.getLogger("Ansible")
fh = None

def load():
    global fh
    fh = logging.FileHandler('logs/ansible.log')
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    logger.info("Loaded")

def unload():
    global fh
    logger.removeHandler(fh)

@hookpoint('divvycloud.instance.modified')
def handle_modified_instance(resource, old_resource=None, user_resource_id=None):

    try:
        logger.info("Detected instance modified")
        if (resource.instance.tags.tags == None):
            logger.error("Resource has no tags [ %s ] " % resource.instance.name)
            return 

        tags = json.loads(resource.instance.tags.tags)
        logger.info("Looking at tags")

        if tags.has_key("environment"):
            env_name= tags.get("environment","No Environment")
            resource_group = ResourceOperations_ResourceGroup.get_by_name(organization_id = 2 , resource_group_name = env_name)
            if(resource_group == None):
                logger.error("Unable to find resource group for environment [%s] " % (env_name))
                return

            if(resource_group.contains_resource(resource.resource_id)):
                logger.error("Unable to add resource, resource already exists")

            logger.info("Adding resource to group [%s] [%s]" % (resource.instance.name,env_name))
            resource_group.add_resource_to_group(resource.resource_id)
    except Exception,e:
        logger.exception(e)

    logger.info("Added resource to group [%s] [%s]" % (resource.instance.name,env_name))

    return


@hookpoint('divvycloud.resourcegroup.modified')
def handle_resource_group_modification(resource, old_resource=None, user_resource_id=None):
    logger.info('Resource Group Modified')

