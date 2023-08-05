import SimpleWorkspace as sw
from datetime import datetime 
import os 

class Log:
    _logPath = None
    @staticmethod
    def Debug(message: str):
        Log.__writeToLog("Debug", message)

    @staticmethod
    def Info(message: str):
        Log.__writeToLog("Info", message)

    @staticmethod
    def Warn(message: str):
        Log.__writeToLog("Warn", message)

    @staticmethod
    def Error(message: str):
        Log.__writeToLog("Error", message)

    @staticmethod
    def __writeToLog(typeOfMessage: str, message: str):
        if(Log._logPath == None):
            Log._logPath = os.path.join(sw.App.path_currentAppData, "info.log")
        logMsg = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f") + f" [{typeOfMessage}] " + message + "\n"
        sw.File.Append(Log._logPath, logMsg)
