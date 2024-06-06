import uuid
from util import FormatUtil

sessions = {}


def getUser(sessionid):
    return sessions[sessionid]


def setUser(userinfo):
    userinfo['session_time'] = FormatUtil.getCurrentTimeStamp()
    sessionId = str(uuid.uuid4())
    userinfo['session_id'] = sessionId
    sessions[userinfo['idkey']] = userinfo
    return sessionId

# def startCheckSession():


