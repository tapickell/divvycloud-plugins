from DivvyPlugins.hookpoints import hookpoint
from DivvyUtils.mail import send_email

@hookpoint('divvycloud.instance.modified')
def instance_modified(resource, old_resource_data, user_resource_id=None):
	send_email(subject="Instance started",
               message="Instance [%s] was started." % (resource.resource_id),
               from_email='test@test.com',
               recipient_list=['your@email.com'],
               organization_id=resource.get_organization_id())

