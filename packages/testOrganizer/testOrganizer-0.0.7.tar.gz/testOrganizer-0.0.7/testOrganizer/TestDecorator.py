import traceback
import time
from datetime import datetime

from testOrganizer.CMDLog import CMDLog

beforeEach = [lambda: print("fd")]
afterEach= [lambda: print("fddf")]
testResult=None

def test(*args, **kwargs):
    """
    Parameters dsc, should_execute, info, browsers
    :param args:
    :param kwargs:
    :return:
    """
    def wrapper(func):
        if len(args) == 0 and kwargs["dsc"]==None:
            raise Exception("Please provide test description")
        try:
            if kwargs["should_execute"]!=None:
                shouldExecute = kwargs["should_execute"]
        except:
            shouldExecute = True


        if len(args)==1:
            dsc = args[0]
        else:
            dsc = kwargs["dsc"]

        try:
            if kwargs["info"] != None:
                info = kwargs["info"]
        except:
            info = ""
        condition_messages=""
        try:
            if kwargs["post_conditions"]!=None:
                conditions = kwargs["post_conditions"]
                if conditions:
                    condition_messages = "*******   State of test user is changed. Actions are required!   **********"
        except:
            conditions = False

        startDateTime = datetime.now()
        startDateTime = str(startDateTime).split(".")[0]
        if shouldExecute:
            startTime = time.time()
            try:
                timeToSubstract = 0
                if beforeEach!=None:
                    startTimeb = time.time()
                    beforeEach[0]()
                    endTimeb = time.time()
                    timeToSubstract += endTimeb-startTimeb
                func()
                if afterEach!=None:
                    startTimea = time.time()
                    afterEach[0]()
                    endTimea = time.time()
                    timeToSubstract += endTimea-startTimea
                endTime = time.time()
                duration = endTime - startTime - timeToSubstract
                testResult = (func.__name__, dsc, "Sucedded. {}".format(info), startDateTime, str(duration).split(".")[0])
            except Exception as e:
                print(e)
                endTime = time.time()
                duration = endTime - startTime
                testResult = (func.__name__, dsc, "Failed. Info: " + info + "\n" + condition_messages + "\n\n" + traceback.format_exc(), startDateTime, str(duration).split(".")[0])
                tb=traceback.format_exc().splitlines()
                k=func.__name__ + " failed: <br>"
                for t in tb:
                    k += t+"<br>"
        else:
            if info != "":
                result = "NOT EXECUTED. Reason: {}".format(info)
            else:
                result = "NOT EXECUTED"
            testResult = (func.__name__, dsc, result, str(startDateTime), "0")

        if CMDLog.testResults!=None:
            CMDLog.testResults.append(testResult)
        else:
            CMDLog.testResults=[testResult]

    return wrapper


def beforeEachTest():
    def wrapper(func):
        beforeEach[0]=func
    return wrapper


def afterEachTest():
    def wrapper(func):
        afterEach[0]=func
    return wrapper

def print_result():
    CMDLog.print_result()

def print_html(suite, url):
    CMDLog.log_html(suite, url)