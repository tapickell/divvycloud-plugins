'''
Simple slack notifier for resource changes
'''

import simplejson as json
import requests
from DivvyPlugins.hookpoints import hookpoint

def send_to_slack(channel, username, message):
    '''
    Send a message to slack.
    '''

    # Slack webhook URL
    slack_webhook = 'https://hooks.slack.com/services/your/slack/api/code/goes/here/'
    slack_webhook = 'https://hooks.slack.com/services/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'

    if slack_webhook is None:
        raise Exception("Slack webhook URI is not configured!")

    # Form slack payload
    payload = {
        'channel': channel,
        'username': username,
        'text': message
    }

    data = json.dumps(payload)
    requests.post(slack_webhook, data=data)


@hookpoint('divvycloud.resource.created')
def resource_created(resource, user_resource_id=None, project_resource_id=None):  # pylint: disable=W0613

 
    #Create our message
    message = 'Resource %s [%s] was created' % (resource.get_resource_name(),resource.get_resource_id())

    # Notify via slack
    send_to_slack(channel='#divvy-development',username="DivvyCloud",message=message)
 

@hookpoint('divvycloud.resource.destroyed')
def resource_destroyed(resource, user_resource_id=None):  # pylint: disable=W0613
 
    #Create our message
    message = 'Resource %s [%s] was destroyed' % (resource.get_resource_name(),resource.get_resource_id())

    # Notify via slack
    send_to_slack(channel='#divvy-development',username="DivvyCloud",message=message)
 

@hookpoint('divvycloud.resource.modified')
def resource_modified(resource, old_resource_data, user_resource_id=None):  # pylint: disable=W0613

 
    #Create our message
    message = 'Resource %s [%s] was modified' % (resource.get_resource_name(),resource.get_resource_id())

    # Notify via slack
    send_to_slack(channel='#divvy-development',username="DivvyCloud",message=message)
 

