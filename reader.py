import sys
import collections


# Here the html page is designed
#-----------------------------------------------------------------------------------------
html_start = """
<html>
<head>
    <title>JTL Dashboard</title>
    <style>
        body {font-family: Arial;} 
        table {
            margin-bottom: 10px;
            border-collapse: collapse;
            min-width: 650px;
        }
        #table {overflow-x:auto;}
        th {background-color: #0b5b85;
            color: #fff;
        }
        .fail {background-color: #ec8484;}
        th, td {
            border: 1px solid #cecfd5;
            padding: 10px 15px;
            text-align: center;
        }
        .card {
            min-width: 150px;
            height: 50px;
            color: white;
            background-color: #05527b;
            border: 1px solid grey;
            border-radius: 5px;
            text-align: center;
            margin-bottom: 10px;
        }
        .card > p { vertical-align: middle;}
        .this {
            text-align: left;
            min-width: 350px;
        }
        .side { min-width: 150px;}
        .red {color:#ec8e8e;} 
        .green {color: green;}
        a {text-decoration: none;}
        a:hover{text-decoration:underline;}
    </style>
</head>
"""
html_body = """
<body>
    <div id="table">
    <center>
    <div class="card">
        <p class="pagetitle">
"""
html_end = """
        </center>
    </body>
</html>
"""
# ----------------------------------------------------------------------------------------

def extract_info(filename):
    required_fields = []
    output = {}
    with open(filename, 'r') as jtl_file:
        for rows in jtl_file:
            temp = rows.split(',')
            required_fields.append([temp[2], temp[8]])
    required_fields.pop(0)
    env_info = [0, 0]
    for each_list in required_fields:
        pcount, fcount = 0, 0
        temp = each_list[0].split('_', 1)
        env_info[0] = len(temp[0]) if len(temp[0]) > env_info[0] else env_info[0]
        env_info[1] = len(temp[1]) if len(temp[1]) > env_info[1] else env_info[1]
        if temp[0] in output:
            if temp[1] in  output[temp[0]]:
                pcount, fcount = output[temp[0]][temp[1]]
            if each_list[1] == 'true':
                pcount += 1
            else:
                fcount += 1
            output[temp[0]][temp[1]] = [pcount, fcount]
        else:
            if each_list[1] == 'true':
                pcount = 1
            else:
                fcount = 1
            output[temp[0]]= {temp[1]: [pcount, fcount]}
    return collections.OrderedDict(sorted([k, sorted(v.items())] for k, v in output.items())), env_info

def print_table(filename, content, info):
    for k, v in  content.items():
        curr = content[k]
        rowspan = len(curr)
        print("\nFor TestCase: " + str(k).upper())
        print("URL" + " "*9 + ": jive.fico.com")
        boundary = info[1] + 15 + 15 + 5 + 10
        print("-"*boundary)
        print("Use Case".center(info[1] + 5) + "|" + "Total".center(15) + "|" + "Failed".center(15) + "|")
        print("-"*boundary)
        for temp in curr:
            a, pf = temp
            s = str(pf[0]+pf[1])
            print(a.center(info[1] + 5) + "|" + s.center(15) + "|" +  str(pf[1]).center(15) + "|")
        print("-"*boundary)



def create_html(filename, content, html_file_name):
    global html_body, html_end, html_start
    
    html_body += "<b>Result for: </b>" + str(filename) + "</p></div>"

    for k, v in content.items():
        i = 0
        html_body += """
        <table>
            <tr>
                <th>Test Case #</th>
                <th>Use Case</th>
                <th>Total</th>
                <th>Failed</th>
                <th>URL</th>
            </tr>
        """
        curr = content[k]
        rowspan = len(curr)
        html_body += "<tr><td class=\"side\" rowspan=\"" + str(rowspan) + "\">" + str(k).upper() + "</td>"
        flag = True
        URL="#"
        for temp in curr:
            a, pf = temp
            color = "pass"
            if pf[1] >= 1:
                color = "fail"
            if i > 0:
                html_body += "<tr>"
            i += 1
            html_body += "<td class=\"this " + color + "\">" + str(a) + "</td>"
           
            html_body += "<td class=\"" + color + "\">" + str(pf[1]+pf[0]) + "</td>"
            html_body += "<td class=\"" + color + "\">" + str(pf[1]) +  "</td>"
            if flag == True:
                html_body += "<td rowspan=\"" + str(rowspan) + "\">" + "<a href=\""+URL+"\">" + "Click here!" + "</a></td></tr>"
                flag = False
            else:
                html_body += "</tr>"
        html_body += "</table>"
    with open(html_file_name, "w") as html_file:
        html_file.write(html_start + html_body + html_end)
     

def main(args):
    """This function will get the arguments from the command file and extract the key values
       from the .jtl file and return as a python dictionary"""
    if len(args) != 1:
        print ("[Error] Wrong number of arguments.")
        print ("[Suggestion] Usage > $python reader.py filename.jtl")
        exit(-1)
    filename = args[0]
    html_file_name = "error_log.html"
    content, info = extract_info(filename)
    print_table(filename, content, info)
    create_html(filename, content, html_file_name)
    print ("[Done] The log file " + html_file_name + " is generated as output.")

if __name__ == '__main__':
    # passing all the command line arguments to the main function,
    # argv[0] conatins the file name iteself so no need for that.
    main(sys.argv[1:])
