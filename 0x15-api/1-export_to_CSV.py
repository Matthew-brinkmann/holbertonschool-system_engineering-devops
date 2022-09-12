#!/usr/bin/python3
"""
Using what you did in the task #0,
extend your Python script to export data in the CSV format.
"""
import csv
import requests
import sys


class UserControlObject:
    """
    User class which hadnles the information for current user.
    """
    __instance = None

    def __new__(cls):
        """New class to ensure only 1 instance of controller at a time"""
        if UserControlObject.__instance is None:
            UserControlObject.__instance = super().__new__(cls)
        return UserControlObject.__instance

    def __init__(self):
        """init method to create new dictionaries"""
        self.allUserInformationComplete = "refresh"
        self.allUserIdList = "refresh"
        self.fullTodoInformation = "refresh"

    @property
    def allUserInformationComplete(self):
        """returns all user dictionary"""
        return (self.__allUserList)

    @allUserInformationComplete.setter
    def allUserInformationComplete(self, getAllUserInfromation):
        """sets all user dictionary"""
        if getAllUserInfromation == "refresh":
            self.__allUserList = self.APIcallInterface()

    @property
    def allUserIdList(self):
        """gets the list of available ID's"""
        return (self.__allUserIdList)

    @allUserIdList.setter
    def allUserIdList(self, getAllUserIdList):
        """sets list of avaiable ID's"""
        if getAllUserIdList == "refresh":
            self.__allUserIdList = [
                item['id'] for item in self.allUserInformationComplete
                ]

    @property
    def fullTodoInformation(self):
        """Getter for full todo dictionary"""
        return (self.__fullTodoInformation)

    @fullTodoInformation.setter
    def fullTodoInformation(self, getFullTodoInformation):
        """geter entire todo list from API"""
        if getFullTodoInformation == "refresh":
            self.__fullTodoInformation = \
                self.APIcallInterface(todos=True)

    @property
    def currentSelectedUser(self):
        """getter for current user ID"""
        return (self.__currentSelectedUser)

    @currentSelectedUser.setter
    def currentSelectedUser(self, newSelectedUser):
        """will update the current user information"""
        if newSelectedUser in self.allUserIdList:
            self.__currentSelectedUser = newSelectedUser
            self.__currentUserTodoList = \
                self.__getUserTaskListFromTodoDict(newSelectedUser)
            self.__currentUserCompletedTodoList = \
                self.__getCompletedTaskListFromTodoDict()
            self.__currentUserInformation = \
                self.__getCurrentUserInformation(newSelectedUser)

    @property
    def currentUserTodoList(self):
        """getter for current user entire todo list"""
        return (self.__currentUserTodoList)

    @property
    def currentUserCompletedTodoList(self):
        """getter for current user completed todo items"""
        return (self.__currentUserCompletedTodoList)

    @property
    def currentUserInformation(self):
        """getter for Current user Info"""
        return (self.__currentUserInformation)

    def __getCurrentUserInformation(self, userToSelectList):
        """returns a dictionary containing only completed todo items on list"""
        for user in self.allUserInformationComplete:
            if user.get('id') == userToSelectList:
                return (user)
        return (None)

    def __getUserTaskListFromTodoDict(self, userToSelectList):
        """returns a dictionary containing only completed todo items on list"""
        currentUserTaskList = []
        for task in self.fullTodoInformation:
            if task.get('userId') == userToSelectList:
                currentUserTaskList.append(task)
        return (currentUserTaskList)

    def __getCompletedTaskListFromTodoDict(self):
        """returns a dictionary containing only completed todo items on list"""
        currentUserCompletedTaskList = []
        for task in self.currentUserTodoList:
            if task.get('completed') is True:
                currentUserCompletedTaskList.append(task)
        return (currentUserCompletedTaskList)

    def __str__(self):
        """Prints employee information in correct format"""
        returnString = "Employee {} is done with tasks({}/{}):\n".\
            format(self.currentUserInformation.get('name'),
                   len(self.currentUserCompletedTodoList),
                   len(self.currentUserTodoList))
        returnString += "\n".join("\t {}".format(completedTask.get("title"))
                                  for completedTask
                                  in self.currentUserCompletedTodoList)
        return (returnString)

    def APIcallInterface(self, todos=False):
        """
        This is the API call interface. OPTIONS: TODOS = T/F
        Useage: Default call is https://jsonplaceholder.typicode.com/users
        Will return entire dictionary for either users or Todos.
        """
        if todos is False:
            apiResponse = requests.get(
                            "https://jsonplaceholder.typicode.com/users",
                            verify=False)
        else:
            apiResponse = requests.get(
                            "https://jsonplaceholder.typicode.com/todos",
                            verify=False)
        return (self.parseAPIResponse(apiResponse))

    def parseAPIResponse(self, apiResponseObject):
        """Will convert API responce to a dictionary"""
        try:
            apiResponseDictionary = apiResponseObject.json()
        except ValueError:
            print("Error Converting API resonse to Dictionary")
            sys.exit()
        return (apiResponseDictionary)

    def writeToCSVFileRows(self, csvWriter):
        """Will write each line to a CSV file"""
        userName = self.currentUserInformation.get('name')
        for task in self.currentUserTodoList:
            csvWriter.writerow([self.currentSelectedUser,
                                userName,
                                task.get('completed'),
                                task.get('title')])

    def exportTodoListForUserAsCSV(self):
        """Prints user information in correct format"""
        with open("{}.csv".format(self.currentSelectedUser),
                  'w',
                  newline='') as csvfile:
            csvWriter = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
            self.writeToCSVFileRows(csvWriter)


def getCurrentUserId():
    """returns current user ID"""
    if sys.argv[1].isdigit():
        return (int(sys.argv[1]))
    else:
        return (None)


if __name__ == "__main__":
    userController = UserControlObject()
    userController.currentSelectedUser = getCurrentUserId()
    userController.exportTodoListForUserAsCSV()
