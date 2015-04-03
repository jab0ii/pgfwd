# Authors: Jay Kong, Noah Gold, Eric Jan

from django.db import models
from eventhandlers.models import EventHandlerData, HierarchyExhausted
from pageitforward.utils import createErrorDict, StatusCode, ErrorCode
import eventProcessor
from django.utils import timezone
from datetime import datetime    




class EventData(models.Model):

    uuid = models.CharField(max_length=36, unique=True)
    title = models.TextField()
    message = models.TextField()
    handler = models.ForeignKey(EventHandlerData)
    currentPos = models.IntegerField()
    status = models.IntegerField()


    def __unicode__(self):
        return str(self.id)

    @staticmethod
    def getEventStatus(uuid):
        """
        Given an event UUID, returns its status, if one exists.

        Args:
            uuid (str): the uuid identifying the event

        Returns:
            {'acked': boolean,
             'error': Error object}
        """
        event = EventData.objects.filter(uuid=uuid)
        if event.count() == 1:
            return {'acked': event[0].status == StatusCode.ACKED,
                    'error': None}
        else:
            return {'acked': None,
                    'error': createErrorDict(title='Event does not exist.')}

    @staticmethod
    def getEscalationData(uuid):
        """
        Given an event UUID, returns its escalation data.

        Args:
            uuid (str): the uuid identifying the event

        Returns:
            {'acked': boolean,
             'users': [UserPCM objects],
             'error': Error object}
        """
        event = EventData.objects.filter(uuid=uuid)
        if event.count() == 1:
            event = event[0]

            # Event already acked, we are done
            if event.status == StatusCode.ACKED:
                return {'acked': True, 'users': None, 'error': None}

            # Event is active, get the next users to page
            elif event.status == StatusCode.ACTIVE:
                try:
                    newPos = event.currentPos + 1

                    # Get the users as UserPCM dicts
                    pcmUsers = event.handler.getUserPCMOfLevel(newPos)
                    dictUsers = []
                    for user in pcmUsers:
                        dictUsers.append(user.toDict())

                    # Get the timeout and update our position in the event
                    # handler
                    timeout = event.handler.getEscalateTimeOfLevel(newPos)
                    event.currentPos = newPos
                    event.save()
                    return {'acked': False, 'users': dictUsers,
                            'timeout': timeout, 'error': None}

                except HierarchyExhausted:
                    return {'acked': False, 'users': None, 'error':
                            createErrorDict(title='Hierarchy exhausted',
                                            errorCode=ErrorCode.HIER_EXHAUSTED
                                            )
                            }
            else:
                return {'acked': None, 'users': None,
                        'error': createErrorDict(title='Invalid event status.',
                                                 errorCode=event.status)}
        else:
            return {'acked': None, 'users': None,
                    'error': createErrorDict(title='Event does not exist.')}
