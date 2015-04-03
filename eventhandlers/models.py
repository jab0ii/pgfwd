# Authors: Jay Kong, Noah Gold

from django.db import models
from orgs.models import OrgData
from users.models import UserData
from pageitforward.utils import ObjectDoesNotExist, StatusCode
import json


class HierarchyLevelDoesNotExist(Exception):
    pass


class HierarchyExhausted(Exception):
    pass


class EventHandlerData(models.Model):
    title = models.TextField()
    hierarchy = models.TextField()
    org = models.ForeignKey(OrgData)
    status = models.IntegerField(default=StatusCode.ACTIVE)

    def __unicode__(self):
        return str(self.id)

    def getUserPCMOfLevel(self, level):
        """
        Given a level, returns the UserPCM objects of all users in that level
        of the hierarchy.

        EX: Hierarchy layoutLayout of the Json object
        {
            "numLevels":1,
            "levels":
            {
                "0":
                {
                    "timeout":30,
                     "users":[1, 2, 3]
                }
            }
        }

        Args:
            level (int): level of the particular hierarchy you want

        Returns:
            users (list): list of user PCM objects
        """
        users = []
        handlerHierarchy = json.loads(self.hierarchy)

        # Does this level exist?
        if level >= handlerHierarchy['numLevels']:
            raise HierarchyExhausted()

        # There are no negative levels.
        if level < 0:
            raise HierarchyLevelDoesNotExist('Invalid level in hierarchy')

        for userID in handlerHierarchy['levels'][str(level)]['users']:
            thisUser = UserData.objects.get(pk=userID).toUserPCM()
            users.append(thisUser)

        return users

    def getEscalateTimeOfLevel(self, level):
        """
        Given a level, returns the timeout for that level.

        Args:
            level (int): level of the particular hierarchy you want

        Returns:
            escalateTime (int): the timeout for each level
        """
        handlerHierarchy = json.loads(self.hierarchy)

        if str(level) not in handlerHierarchy['levels']:
            raise HierarchyLevelDoesNotExist('Invalid level in hierarchy')

        return handlerHierarchy['levels'][str(level)]['timeout']

    def toDict(self):
        """
        Converts the event handler into a dict representation.
        """
        return {'eventHandlerID': self.pk, 'title': self.title,
                'hierarchy': json.loads(self.hierarchy),
                'orgID': self.org.pk}

    @staticmethod
    def getByID(handlerID):
        """
        Gets an event handler by ID. Throws ObjectDoesNotExist if no such
        handler exists.

        Args:
            handlerID (int): id of the handler to get

        Returns:
            the handler with the given ID if it exists.
        """
        handlers = EventHandlerData.objects.filter(pk=handlerID)
        if handlers.count() == 1:
            return handlers[0]
        else:
            raise ObjectDoesNotExist()

    @staticmethod
    def updateHandler(handlerID, title, hierarchy):
        """
        Tries to update the handler with the given ID to have
        the provided title and hierarchy.

        Args:
            handlerID (int): id of the handler to edit
            title (str):     new title for the handler
            hierarchy (dict): new hierarchy for the handler
        """
        handler = EventHandlerData.getByID(handlerID)
        handler.title = title
        handler.hierarchy = json.dumps(hierarchy)
        handler.save()

    @staticmethod
    def deleteHandler(handlerID):
        handler = EventHandlerData.getByID(handlerID)
        handler.status = StatusCode.INACTIVE
        handler.save()

    @staticmethod
    def createHandler(title, hierarchy, org):
        """
        Creates an event handler with the given parameters and
        returns it.

        Args:
            title (str):      handler title
            hierarchy (dict): Dict representation of the hierarchy to create.
            org (OrgData):    Org that will own the hierarchy

        Returns:
            EventHandlerData for the new handler.
        """
        # TODO: Validate the hierarchy
        handler = EventHandlerData.objects.create(
            title=title,
            hierarchy=json.dumps(hierarchy), org=org,
            status=StatusCode.ACTIVE)
        return handler
