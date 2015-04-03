from events.models import EventData
from events.data_ex import EventDetails
from eventhandlers.models import EventHandlerData
from users.models import UserData, ContactMethodData
from orgs.models import OrgData
from pageitforward.utils import StatusCode
import uuid
import json


def createTestData(obj):
    """
    Creates a set of test data and attaches it
    to the given object as attributes.
    """
    # TODO: Convert this to a fixture
    # Create the org
    org = OrgData.objects.create(status=1, orgName='Test Org')

    # Create the user
    obj.apiKey = str(uuid.uuid4())
    user = UserData.objects.create(org=org, firstName='Test',
                                   lastName='User', apiKey=obj.apiKey,
                                   email='user1@example.com', status=1)
    obj.userID = user.pk

    # Create the contact method
    ContactMethodData.objects.create(contactData='contact data',
                                     contactType='test', user=user,
                                     priority=0)
    obj.userPCM = user.toUserPCM()

    # Create another user
    user = UserData.objects.create(org=org, firstName='Test',
                                   lastName='User',
                                   apiKey=str(uuid.uuid4()),
                                   email='user2@example.com', status=1)
    secondUserPK = user.pk

    # Create another contact method
    ContactMethodData.objects.create(contactData='contact data escalation',
                                     contactType='test', user=user,
                                     priority=0)
    obj.secondUserPCM = user.toUserPCM()

    # Finally create the handler
    handler = EventHandlerData()
    handler.title = 'Test Handler'
    handler.org = org
    hierarchy = \
        {
            'numLevels': 1,
            'levels':
            {
                '0':
                {
                    'timeout': 0,
                    'users': [obj.userID]
                }
            }
        }
    handler.hierarchy = json.dumps(hierarchy)
    handler.save()
    obj.handlerID = handler.pk

    #Escalation Handler
    handler = EventHandlerData()
    handler.title = 'Test Escalation Handler'
    handler.org = org
    hierarchy = \
        {
            'numLevels': 2,
            'levels':
            {
                '0':
                {
                    'timeout': 0,
                    'users': [obj.userID]
                },
                '1':
                {
                    'timeout': 0,
                    'users': [secondUserPK]
                }
            }
        }
    handler.hierarchy = json.dumps(hierarchy)
    handler.save()
    obj.escalationHandlerID = handler.pk

    #Test Ack Handler
    handler = EventHandlerData()
    handler.title = 'Test Ack Handler'
    handler.org = org
    hierarchy = \
        {
            'numLevels': 2,
            'levels':
            {
                '0':
                {
                    'timeout': 0,
                    'users': [obj.userID]
                },
                '1':
                {
                    'timeout': 10,
                    'users': [secondUserPK]
                }
            }
        }
    handler.hierarchy = json.dumps(hierarchy)
    handler.save()
    obj.ackHandlerID = handler.pk

    EventData.objects.create(uuid='uuid_active', title='test event',
                             message='test msg', currentPos=0,
                             status=StatusCode.ACTIVE,
                             handler_id=obj.escalationHandlerID)
    obj.details = EventDetails('test event', 'test msg')
