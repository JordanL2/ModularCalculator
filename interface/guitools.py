#!/usr/bin/python3

import cgi


def htmlSafe(text):
    return cgi.escape(str(text)).replace("\n", '<br/>').replace(' ', '&nbsp;')
