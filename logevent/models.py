# Authors: Eric Jan

from django.db import models
from users.models import UserData
from orgs.models import OrgData
from events.models import EventData
from django.utils import timezone
import datetime    
from pageitforward.utils import createErrorDict, StatusCode
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import utc
from decimal import Decimal
import time



# Create your models here.
class InvalidEventException:
    pass

class EventAckedException:
    pass
class LogEvent(models.Model):
    uuid = models.CharField(max_length=36, unique = False)
    orgID = models.IntegerField(null = True)
    user = models.IntegerField(null = True)
    date_created = models.DateTimeField(null = True)
    date_sent = models.DateTimeField(null = True)
    date_ack = models.DateTimeField(null = True)
    log_type = models.IntegerField(null = True)
    time_diff = models.DecimalField(max_digits=100,decimal_places=4, null = True)
    
    def __unicode__(self):
        return str(self.id)
        
    @staticmethod
    def createLog(uuid, time, status, org):
        ackObj = LogEvent.objects.filter(uuid = uuid, log_type = StatusCode.ACKED)
        objs = LogEvent.objects.filter(uuid = uuid, log_type = StatusCode.PAGESENT)
        if ackObj.count() > 0:
            raise EventAckedException()
        
        if ackObj.count() == 0 and status == StatusCode.ACKED:
            obj = objs[0]
            dateCreated = obj.date_created
            dateSent = obj.date_sent
            ackedObj = LogEvent.objects.create(uuid = uuid,
                                               orgID = org,
                                               date_created = dateCreated,
                                               date_sent = dateSent,
                                               date_ack = time,
                                               log_type = status)
            LogEvent.setTimeDiff(uuid)
            return ackedObj
        else:
            newObj = LogEvent.objects.create(uuid = uuid,
                                             orgID = org,
                                             date_created = time,
                                             log_type = status)
            return newObj
    
    #call after ack
    @staticmethod
    def setTimeDiff(uuid):
        events = LogEvent.objects.filter(uuid = uuid, log_type = StatusCode.ACKED)
        if events.count() > 0:
            for event in events:
                event.time_diff = LogEvent.getTimeDiff(uuid)
                event.save()
        else:
            raise InvalidEventException()
    
    @staticmethod
    def getTimeDiff(uuid):
        userEvents = LogEvent.objects.filter(uuid = uuid, log_type = StatusCode.ACKED)
        if userEvents.count() > 0:
            user = userEvents[0]
            dateSent = user.date_sent
            dateAck = user.date_ack
            timediff = dateAck - dateSent
            return timediff.total_seconds()
        else:
            raise InvalidEventException()


    #returns float
    @staticmethod
    def getAvgTimeDiff(userID):
        userEvents = LogEvent.objects.filter(user = userID, log_type = StatusCode.ACKED)
        avgTime = 0.0
        if userEvents.count() == 0:
            raise InvalidEventException()
        if userEvents.count() == 1:
            return userEvents[0].time_diff
        for event in userEvents:
            avgTime = avgTime + float(event.time_diff)
        #print '%.2f' % (float(avgTime)/float(userEvents.count()))
        return float(avgTime)/float(userEvents.count())
 
            
                
    def toDict(self):
        """
        Converts the logEvents into a dict representation.
        """
        try:
            event = EventData.objects.get(uuid = self.uuid)
            title = event.title
        except ObjectDoesNotExist:
            print 'event DNE'
        try:
            orgname = OrgData.objects.get(pk = self.orgID)
            orgN = orgname.orgName
        except ObjectDoesNotExist:
            print 'org DNE'
        if self.date_created is not None:
            c = self.date_created.strftime("%Y-%m-%d %H:%M:%S")
        else:
            c = self.date_created
        if self.date_sent is not None:
            s = self.date_sent.strftime("%Y-%m-%d %H:%M:%S")
        else:
            s = self.date_sent
        if self.date_ack is not None:
            a = self.date_ack.strftime("%Y-%m-%d %H:%M:%S")
        else:
            a = self.date_ack
        return {'title': title, 'uuid': self.uuid,
                'user': self.user,
                'date_created': c ,
                'date_sent': s ,
                'date_ack': a,
                'log_type': self.log_type,
                'time_diff': self.time_diff,
                'orgName': orgN}