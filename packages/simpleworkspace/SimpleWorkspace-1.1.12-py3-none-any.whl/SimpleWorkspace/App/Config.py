import os as _os
import SimpleWorkspace as _sw

class Config:
    appName = None
    appCompany = None
    appTitle = None
    appHash = None
    path_currentAppData = ""
    path_currentAppData_storage = None

    @staticmethod
    def Setup(appName, appCompany=None):
        Config.appName = appName
        Config.appCompany = appCompany
        Config.appTitle = appName
        if appCompany != None:
            Config.appTitle += " - " + appCompany
        Config.path_currentAppData = _sw.Path.GetAppdataPath(appName, appCompany)
        Config.path_currentAppData_storage = _os.path.join(Config.path_currentAppData, "storage")
        _sw.Directory.Create(Config.path_currentAppData_storage)
        
        _sw.App.Log._logPath = _os.path.join(Config.path_currentAppData, "info.log")
        _sw.App.SettingsManager._settingsPath = _os.path.join(Config.path_currentAppData, "config.json")
        _sw.App.SettingsManager.LoadSettings()
