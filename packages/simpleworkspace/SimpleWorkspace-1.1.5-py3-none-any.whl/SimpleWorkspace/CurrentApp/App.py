import os as _os
import SimpleWorkspace as _sw

class App:
    appName = None
    appCompany = None
    appTitle = None
    appHash = None
    path_currentAppData = ""
    path_currentAppData_storage = None

    @staticmethod
    def Setup(appName, appCompany=None):
        App.appName = appName
        App.appCompany = appCompany
        App.appTitle = appName
        if(appCompany != None):
            App.appTitle += " - " + appCompany
        App.path_currentAppData = _sw.Path.GetAppdataPath(appName, appCompany)
        App.path_currentAppData_storage = _os.path.join(App.path_currentAppData, "storage")
        _sw.Directory.Create(App.path_currentAppData_storage)