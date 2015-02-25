from DivvyPlugins.hookpoints import hookpoint
import logging
import simplejson as json
from DivvyResource.ResourceOperations import ResourceOperations_ResourceGroup
from DivvyResource.ResourceOperations import ResourceOperations_Instance
from DivvyResource.ResourceOperations import ResourceOperations
from DivvyResource import ResourceId
from DivvyPermissions import SessionPermissions
from DivvySession import DivvySession
from DivvyDb.DivvyInterfaceORM  import DivvyInterfaceORM
from DivvyDb import DivvyDb

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




@DivvyDb.SharedSessionScope(DivvyInterfaceORM)
@hookpoint('divvycloud.instance.modified')
def handle_modified_instance(resource, old_resource=None, user_resource_id=None):
    db = DivvyInterfaceORM()
    # Form permissions for session
    # Perform login and get the user data used as the basis for the session
    session_data = db.LoginUser('brian@divvycloud.com')
    user_resource_id = ResourceId.ResourceId_DivvyUser(user_id=1)
    session_permissions = SessionPermissions.SessionPermissions.load_for_user(user_resource_id=user_resource_id)
    DivvySession.create_session(session_permissions=session_permissions, **session_data)


    try:
        logger.info("Detected instance modified [%s]" % (resource.instance.name))
        if (resource.instance.tags.tags == None):
            logger.error("Resource has no tags [ %s ] " % resource.instance.name)
            return

        tags = json.loads(resource.instance.tags.tags)
        logger.info("Looking at tags")

        if tags.has_key("environment"):
            env_name= tags.get("environment","No Environment")
            resource_group = ResourceOperations_ResourceGroup.get_by_name(organization_id = 1 , resource_group_name = env_name)
            if(resource_group == None):
                logger.error("Unable to find resource group for environment [%s] " % (env_name))
                return


            if(resource_group.contains_resource(resource.resource_id)):
                logger.error("Unable to add resource, resource already exists")
                return

            logger.info("Adding resource to group [%s] [%s]" % (resource.instance.name,env_name))
            resource_group.add_resource_to_group(resource.resource_id)
    except Exception,e:
        logger.exception(e)

    logger.info("Added resource to group [%s] [%s]" % (resource.instance.name,env_name))

    return

@hookpoint('divvycloud.resourcegroup.modified')
def handle_resource_group_modification(resource, old_resource=None, user_resource_id=None):
    try:
        logger.info('Resource Group Modified [%s]' % (resource.get_resource_name()))
        new_list = [r.to_string() for r in resource.enumerate_contained_resource_ids()]
        added_resource_ids= (set(new_list) -  set(old_resource))


        for add_resource_id in added_resource_ids:
            new_resource_id = ResourceId.ResourceId.from_string(add_resource_id)
            new_resource = ResourceOperations.from_resource_id(new_resource_id)
            if(new_resource.get_resource_type() == 'instance'):
                logger.info("Added : [%s] [%s]" % (new_resource.instance.name,new_resource.get_attached_public_ips() ))


    except Exception,e:
        logger.error("FAILE [%s]" %(e))