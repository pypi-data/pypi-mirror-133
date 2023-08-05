import os
import sys

from tabulate import tabulate


class CMDLog:


    testResults = None

    @staticmethod
    def print_result():
        helpVariable = []
        fulltime = 0
        for tr in CMDLog.testResults:
            fulltime += int(tr[4])
            helpVariable.append([tr[0],tr[1], tr[2], tr[3], tr[4]])
        helpVariable.append(["","","","", str(fulltime)])
        final_result = str(tabulate(helpVariable, headers=["Test link ID", "Test description", "Result", "Start time", "Duration"], tablefmt='orgtbl'))
        print("\n")
        print("*************"+os.path.basename(sys.argv[0])+"*****************")
        print("\n")
        print(tabulate(helpVariable, headers=["Test link ID", "Test description", "Result", "Start time", "Duration"]))

