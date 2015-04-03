# Authors: Jay Kong, Noah Gold

"""
Contains data exchange objects for users.
"""


class ContactMethod:

    def __init__(self, user, contactType, contactData, priority,
                 contactMethodID, title):
        """
        Creates a ContactMethod object.

        Args:
            user (int): the owner of this contact method
            contactType(str): contact type
            contactData(str): contact data
            priority (int): priority
            contactMethodID (int): Contact method ID / PK
            title (str): contact title
        """
        self.user = user
        self.contactType = contactType
        self.contactData = contactData
        self.priority = priority
        self.contactMethodID = contactMethodID
        self.title = title

    def toDict(self):
        """
        Returns a dict representation.
        """
        return {'user': self.user,
                'contactType': self.contactType,
                'contactData': self.contactData,
                'priority': self.priority,
                'contactMethodID': self.contactMethodID,
                'title': self.title}

    @staticmethod
    def fromDict(dictData):
        """
        Takes a dict rep. of a ContactMethod and creates the corrasponding
        ContactMethod.

        Args:
            dictData (dict): dict rep. of the ContactMethod to create.

        Returns:
            New ContactMethod matching the dictData.
        """

        return ContactMethod(dictData['user'], dictData['contactType'],
                             dictData['contactData'], dictData['priority'],
                             dictData['contactMethodID'], dictData['title'])


class UserPCM:
    """
    A User and their contact methods.
    """

    def __init__(self, firstName, lastName, status, contactMethods,
                 orgID, apiKey, user):
        """
        Creates a UserPCM object.
        *Note that contactMethods in the raw object forms are not sorted.
         Only the toDict() output is sorted.

        Args:
            firstName (str): user's first name
            lastName (str): user's last name
            status (int): user's status
            contactMethods (list): list of the user's ContactMethods
            orgID (int): user's org ID
        """
        self.firstName = firstName
        self.lastName = lastName
        self.status = status
        self.contactMethods = contactMethods
        self.orgID = orgID
        self.apiKey = apiKey
        self.user = user

    def __eq__(self, other):
        if isinstance(other, UserPCM):
            return cmp(self.toDict(), other.toDict()) == 0
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def toDict(self):
        """
        Returns a dict representation with contactMethods sorted by priority.
        """
        dictObj = {'firstName': self.firstName, 'lastName': self.lastName,
                   'status': self.status, 'orgID': self.orgID,
                   'apiKey': self.apiKey, 'user': self.user,
                   'contactMethods': []}

        if self.contactMethods:
            for contactMethod in self.contactMethods:
                dictObj['contactMethods'].append(contactMethod.toDict())

            dictObj['contactMethods'] = sorted(dictObj['contactMethods'],
                                               key=lambda k: k['priority'])

        return dictObj

    @staticmethod
    def fromDict(dictData):
        """
        Takes a dict rep. of a UserPCM object and returns a new UserPCM object.
        *Note that contactMethods in the raw object forms are not sorted.
         Only the toDict() output is sorted.

        Args:
            dictData (dict): the dict representation

        Returns:
            UserPCM object matching the dictData.
        """
        methods = []
        for contactMethod in dictData['contactMethods']:
            methods.append(ContactMethod.fromDict(contactMethod))

        return UserPCM(dictData['firstName'], dictData['lastName'],
                       dictData['status'], methods, dictData['orgID'],
                       dictData['apiKey'], dictData['user'])
