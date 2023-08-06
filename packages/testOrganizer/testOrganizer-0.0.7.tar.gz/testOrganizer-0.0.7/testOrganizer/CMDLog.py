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

    @staticmethod
    def log_html(suiteName, url):
        with open(url, 'a') as f:
            fulltime = 0
            finalString="<h3>"+suiteName+"</h3><br>"
            finalString+="""<table style='border: 1px solid #ddd;border-collapse: collapse;width:50%;'>"""
            finalString+= """<tr style='border: 1px solid #ddd;'>
            <td>Test name</td>
            <td>Description</td>
            <td>Result</td>
            <td>Start time</td>
            <td>Duration</td>
            </tr>"""
            for tr in CMDLog.testResults:
                fulltime += int(tr[4])
                testLinkId = tr[0]
                dsc = tr[1]
                result=tr[2]
                startTime=tr[3]
                duration=tr[4]
                if "failed" in result.lower():
                    finalString += "<tr style='border: 1px solid #ddd;background-color:#EE4B2B;word-wrap:break-word'>"
                elif "not executed" in result.lower():
                    finalString += "<tr style='border: 1px solid #ddd;background-color:#ffffc4;word-wrap:break-word'>"
                else:
                    finalString += "<tr style='border: 1px solid #ddd;word-wrap:break-word'>"
                finalString += "<td>"+testLinkId+"</td>"
                finalString += "<td>"+dsc+"</td>"
                finalString += "<td>"+result+"</td>"
                finalString += "<td>"+startTime+"</td>"
                finalString += "<td style='text-align: center;'>"+duration+"</td>"
                finalString += "</tr>"

            finalString+="""<tr style='border: 1px solid #ddd;'>
            <td>Full duration</td>
            <td></td>
            <td></td>
            <td></td>
            <td style='text-align: center;'>{}</td>
            </tr>""".format(str(fulltime))
            finalString+="</table>"
            f.writelines(finalString)



