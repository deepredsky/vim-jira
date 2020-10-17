# -*- coding: utf-8 -*-

import textwrap
import collections
import json
import vim
import webbrowser
import urllib.request, urllib.error, urllib.parse
import re
import os
import base64

class NestedDict(dict):
    def get(self, path, default = None):
        keys = path.split(".")
        val = None

        for key in keys:
            if val:
                if isinstance(val, list):
                    val = [ v.get(key, default) if v else None for v in val]
                else:
                    val = val.get(key, default)
            else:
                val = dict.get(self, key, default)

            if not val:
                break;

        return val

def jira_search_url():
    return vim.eval('g:jira_url') + '/rest/api/latest/search?fields=summary,priority,status,creator,assignee,issuetype'

def jira_sprint_issues_url(board_id, sprint_id=None):
    if not sprint_id:
        sprint_id = get_current_sprint_id(board_id)

    api_url = vim.eval('g:jira_url') + '/rest/api/latest/search?jql=Sprint=' + str(sprint_id) + '&fields=summary,priority,status,creator,assignee,issuetype'
    return api_url

def get_current_sprint_id(board_id):
    api_url = vim.eval('g:jira_url') + '/rest/agile/1.0/board/' + str(board_id) + '/sprint?state=active'

    try:
        current_sprint = load_jira(api_url)
    except:
        print('vim-jira error: could not find current sprint for board ' + str(board_id))

    return current_sprint['values'][0]['id']

def bufwrite(string):
    b = vim.current.buffer

    # Never write more than two blank lines in a row
    if not string.strip() and not b[-1].strip() and not b[-2].strip():
        return

    # Vim must be given UTF-8 rather than unicode
    if isinstance(string, str):
        string = string.encode('utf-8', errors='replace')

    # Code block markers for syntax highlighting
    if string and string[-1] == chr(160).encode('utf-8'):
        b[-1] = string
        return

    if not b[0]:
        b[0] = string
        return

    if not b[0]:
        b[0] = string
    else:
        b.append(string)

def read_url(url):
    http_handler = urllib.request.HTTPHandler(debuglevel=4)
    opener = urllib.request.build_opener(http_handler)
    username = os.environ.get('JIRA_USERNAME')
    password = os.environ.get('JIRA_API_TOKEN')
    headers = []
    if username is not None and password is not None:
        data_string = username + ":" + password
        base64string = base64.b64encode(data_string.encode("utf-8"))
        opener.addheaders = [("Authorization", "Basic %s" % base64string)]
        headers.append(("Authorization", "Basic %s" % base64string.decode("utf-8")))
    headers.append(('Content-Type', 'application/json'))
    opener.addheaders = headers
    return opener.open(url).read()

def load_jira(url):
    try:
        return json.loads(read_url(url))
    except:
        print('vim-jira error: could not connect to JIRA server')

urls = [None] * 1000 # urls[index]: url of link at index

def vim_jira_sprint(sprint_id):
    board_id = vim.eval('g:jira_board_id')
    url = jira_sprint_issues_url(board_id, sprint_id)
    vim_jira(url)

def vim_jira(url = None):
    if url is None:
        url = jira_search_url()

    items = load_jira(url)
    if items is not None:
        vim.command('edit .jira')
        vim.command('setlocal buftype=nofile bufhidden=wipe noswapfile nomodeline')

        bufwrite("   ___ _             _____")
        bufwrite("  |_  (_)           |_   _|")
        bufwrite("    | |_ _ __ __ _    | | ___ ___ _   _  ___  ___")
        bufwrite("    | | | '__/ _` |   | |/ __/ __| | | |/ _ \/ __|")
        bufwrite("/\__/ / | | | (_| |  _| |\__ \__ \ |_| |  __/\__ \\")
        bufwrite("\____/|_|_|  \__,_|  \___/___/___/\__,_|\___||___/")

        bufwrite('')
        bufwrite('')

        for i, item in enumerate(items['issues']):
            try:
                line_1 = build_header_line(i, item)
                line_2 = '    ' + build_summary_line(item)
                bufwrite(line_1)
                bufwrite(line_2)
                bufwrite('')

                urls[i + 1] = item['self']
            except KeyError:
                pass

def build_header_line(i, item):
    # surround shorter numbers (e.g. 9) with padding
    # to align with longer numbers
    index = (2 - len(str(i + 1))) * ' ' + str(i + 1) + '. '

    heading_line = index + item['key'] + ' : ' + item['fields']['summary']
    return heading_line

def build_summary_line(item):
    summary_items = []
    labels = [
            'Type'    ,
            'Priority',
            'Status'  ,
            'Reporter',
            'Assignee',
            ]
    values = [ get_nested_value(item, 'fields.issuetype.name'),
            get_nested_value(item, 'fields.priority.name'),
            get_nested_value(item, 'fields.status.name'),
            get_nested_value(item, 'fields.creator.name'),
            get_nested_value(item, 'fields.assignee.name') ]
    elms = collections.OrderedDict(list(zip(labels, values)))
    for k in list(elms.keys()):
        if elms[k] is not None:
            summary_items.append(k + ': ' + elms[k])
    return ' | '.join(summary_items)

def get_nested_value(data, path):
    return NestedDict(data).get(path)

def vim_jira_link(line, in_browser = False):
    regexp = re.compile(r'\d+\.')
    if regexp.search(line) is not None:
        id = line.split()[0].replace('.', '')
        if in_browser:
            browser = webbrowser.get()
            browser.open(urls[int(id)])
            return
        item = load_jira(urls[int(id)] + '?fields=summary,description,comment')
        if item is not None:
            try:
                line_1 = item['key'] + ' : ' + item['fields']['summary']

                bufwrite(line_1)
                bufwrite('')

                line_2 = item['fields']['description']
                if line_2 is not None:
                    t = line_2.replace("\\r", "").replace("\\n", "\n").replace("\r", "").split("\n")
                    for wrap in t:
                        bufwrite(wrap)
            except:
                print('vim-jira error: could not parse item')
