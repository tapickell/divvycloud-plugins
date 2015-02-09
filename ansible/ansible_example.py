from DivvyPlugins.hookpoints import hookpoint
import logging
import simplejson as json
from datetime import datetime
import DivvyDb
from DivvyDb import DivvyInterfaceORM
from DivvyDb import DivvyDbObjects



logger = logging.getLogger("Ansible")
fh = None

def load():
    global fh

def unload():
    global fh
    logger.removeHandler(fh)

@DivvyDb.SharedSessionScope(DivvyInterfaceORM.DivvyInterfaceORM)
@hookpoint('divvycloud.instance.create')
def handle_new_instance(resource,user_resource_id=None):

    if (resource.tags.tags == None):
        logger.error("Resource has no tags [ %s ] " % resource.instance.name)

    tags = json.loads(resource.tags.tags)

    if tags.has_key("environment"):
        env = tags.get("environment","No Environment")
        db = DivvyInterfaceORM.DivvyInterfaceORM()
        resource_groups = db.session.query(DivvyDbObjects.ResourceGroup).\
                    filter(DivvyDbObjects.ResourceGroup == env).\
                    all()


        resource_group = resource_groups[0]
        resource_group_id = resource_group["resource_group_id"]

        resource_id = resource.resource_id
        db.AssociateResourceToResourceGroup(2, resource_group_id=resource_group_id, resource_id=resource_id)

@hookpoint('divvy.resource_group.modified'):
def handle_resource_group_modification(resource,old_resource,user_resource_id=None):
    logger.info("Resource group has been modified")












