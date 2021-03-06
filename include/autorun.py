import os, json, configparser, webbrowser, traceback, urllib.parse, itertools
import ts3defines, ts3lib, ts3client, ts3help, ts3Ext, pytson, pytsonui
from datetime import datetime
from ts3lib import *
from ts3plugin import *
from pytsonui import *
from ts3defines import *
from devtools import *
from ts3help import *
from ts3client import *
from PythonQt.QtGui import *
from PythonQt.QtCore import *
from PythonQt.QtNetwork import *
from PythonQt.Qt import *
from PythonQt.private import *
from PythonQt.QtSql import *
from PythonQt.QtUiTools import *
from bluscream import *

self = QApplication.instance()

urlrequest = False
def url(url):
    try:
        from PythonQt.QtNetwork import QNetworkAccessManager, QNetworkRequest
        #if urlrequest: return
        urlrequest = QNetworkAccessManager()
        urlrequest.connect("finished(QNetworkReply*)", urlResponse)
        urlrequest.get(QNetworkRequest(QUrl(url)))
    except:
        from traceback import format_exc
        try: ts3lib.logMessage(format_exc(), ts3defines.LogLevel.LogLevel_ERROR, "PyTSon::autorun", 0)
        except: print("Error in autorun: "+format_exc())
def urlResponse(reply):
    try:
        from PythonQt.QtNetwork import QNetworkReply
        if reply.error() == QNetworkReply.NoError:
            print("Error: %s (%s)"%(reply.error(), reply.errorString()))
            print("Content-Type: %s"%reply.header(QNetworkRequest.ContentTypeHeader))
            print("<< reply.readAll().data().decode('utf-8') >>")
            print("%s"%reply.readAll().data().decode('utf-8'))
            print("<< reply.readAll().data() >>")
            print("%s"%reply.readAll().data())
            print("<< reply.readAll() >>")
            print("%s"%reply.readAll())
            return reply
        else:
            err = logMessage("Error checking for update: %s" % reply.error(), ts3defines.LogLevel.LogLevel_ERROR, "pyTSon.PluginHost.updateCheckFinished", 0)
            if err != ts3defines.ERROR_ok:
                print("Error checking for update: %s" % reply.error())
        urlrequest.delete()
    except:
        from traceback import format_exc
        try: ts3lib.logMessage(format_exc(), ts3defines.LogLevel.LogLevel_ERROR, "PyTSon::autorun", 0)
        except: print("Error in autorun: "+format_exc())

def findWidget(name):
    try:
        name = name.lower()
        widgets = self.topLevelWidgets()
        widgets = widgets + self.allWidgets()
        ret = dict()
        c = 0
        for x in widgets:
            c += 1
            if name in x.objectName.lower() or name in str(x.__class__).lower():
                ret["class:"+str(x.__class__)+str(c)] = "obj:"+x.objectName;continue
            if hasattr(x, "text"):
                if name in x.text.lower():
                    ret["class:"+str(x.__class__)+str(c)] = "obj:"+x.objectName
        return ret
    except:
        print("error")
def widgetbyclass(name):
    ret = []
    widgets = self.topLevelWidgets()
    widgets = widgets + self.allWidgets()
    for x in widgets:
        if name in str(x.__class__).replace("<class '","").replace("'>",""):
            ret.extend(x)
    return ret
def widgetbyobject(name):
    name = name.lower()
    widgets = self.topLevelWidgets()
    widgets = widgets + self.allWidgets()
    for x in widgets:
        if str(x.objectName).lower() == name:
            return x


def file(name, content):
    with open(os.path.expanduser("~/Desktop/"+name+".txt"), "w") as text_file:
        print(str(content), file=text_file)

def getvar(clid):
    for name, var in getItems(ConnectionProperties) + getItems(ConnectionPropertiesRare):
        ret = "=== Results for {0} ===\n".format(name)
        try:
            (err, var1) = getConnectionVariableAsDouble(schid, clid, var)
            (er, ec) = getErrorMessage(err)
            ret += "getConnectionVariableAsDouble: err={0} var={1}\n".format(ec, var1)
        except Exception as e:
            ret += "getConnectionVariableAsDouble err={0}\n".format(e)
        try:
            (err, var2) = getConnectionVariableAsUInt64(schid, clid, var)
            (er, ec) = getErrorMessage(err)
            ret += "getConnectionVariableAsUInt64: err={0} var={1}\n".format(ec, var2)
        except Exception as e:
            ret += "getConnectionVariableAsUInt64 err={0}\n".format(e)
        try:
            (err, var3) = getConnectionVariableAsString(schid, clid, var)
            (er, ec) = getErrorMessage(err)
            ret += "getConnectionVariableAsString: err={0} var={1}\n".format(ec, var3)
        except Exception as e:
            ret += "getConnectionVariableAsString err={0}\n".format(e)
        print("{0}================".format(ret))

#if error == 0:
    #error, ownnick = getClientDisplayName(schid, ownid)
    # if error == 0:
    #     def p(c, cmd="test", clid=0):
    #         if c == 0:
    #             print("Sent command "+cmd+" to PluginCommandTarget_CURRENT_CHANNEL")
    #         elif c == 1:
    #             print("Sent command "+cmd+" to PluginCommandTarget_SERVER")
    #         elif c == 2:
    #             print("Sent command "+cmd+" to PluginCommandTarget_CLIENT")
    #             sendPluginCommand(schid, cmd, c, [clid])
    #             return
    #         elif c == 3:
    #             print("Sent command "+cmd+" to PluginCommandTarget_CURRENT_CHANNEL_SUBSCRIBED_CLIENTS")
    #         elif c == 4:
    #             print("Sent command "+cmd+" to PluginCommandTarget_MAX")
    #         sendPluginCommand(schid, cmd, c, [])

schid = getCurrentServerConnectionHandlerID()
(_e, ownid) = getClientID(schid)

print('(pyTSon Console started at: {:%Y-%m-%d %H:%M:%S})'.format(datetime.now()))
for item in sys.path:
    print('"'+item+'"')
print("")
print(sys.flags)
print("")
print(sys.executable+" "+sys.platform+" "+sys.version+" API: "+str(sys.api_version))
print("")

class testClass(object):
    def __init__(): pass
    def testFunction(): pass
