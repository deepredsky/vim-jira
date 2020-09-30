# -*- coding: utf-8 -*-

import textwrap
import collections
import json
import vim
import webbrowser
import urllib.request, urllib.error, urllib.parse
import re
import os

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
    opener = urllib2.build_opener()
    username = os.environ.get('JIRA_USERNAME')
    password = os.environ.get('JIRA_PASSWORD')
    if username is not None and password is not None:
        base64string = base64.b64encode('%s:%s' % (username, password))
        opener.add_header("Authorization", "Basic %s" % base64string)
    opener.addheaders = [('User-Agent', 'Python/vim-jira')]
    return opener.open(url.encode("UTF-8")).read()

def load_jira(url):
    try:
        return json.loads(read_url(url))
    except:
        print 'vim-jira error: could not connect to JIRA server'

urls = [None] * 1000 # urls[index]: url of link at index

def vim_jira():
    items = load_jira(jira_search_url())
    if items is not None:
        vim.command('edit .jira')
        vim.command('setlocal noswapfile')
        vim.command('setlocal buftype=nofile')

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

def vim_jira_link(in_browser = False):
    line = vim.current.line
    print((urls[int(line.split()[0].replace('.', ''))]))

    regexp = re.compile(r'\d+\.')
    if regexp.search(line) is not None:
        id = line.split()[0].replace('.', '')
        if in_browser:
            browser = webbrowser.get()
            browser.open(urls[int(id)])
            return
        vim.command('edit .jira')
        item = load_jira(urls[int(id)] + '?fields=summary,description,comment')
        if item is not None:
            try:
                line_1 = item['key'] + ' : ' + item['fields']['summary']

                bufwrite(line_1)
                bufwrite('')

                line_2 = item['fields']['description']
                if line_2 is not None:
                    line_2 = textwrap.wrap(line_2, width=80)
                    for wrap in line_2:
                        bufwrite(wrap)
            except:
                print('vim-jira error: could not parse item')
