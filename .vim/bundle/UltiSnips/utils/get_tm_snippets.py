#!/usr/bin/env python
# encoding: utf-8

import urllib
import re
from xml.etree import ElementTree
from xml.parsers.expat import ExpatError
import htmlentitydefs
import os
import glob


_UNESCAPE = re.compile(ur'&\w+?;', re.UNICODE)
def unescape(s):
    if s is None:
        return ""
    def fixup(m):
        ent = m.group(0)[1:-1]
        return unichr(htmlentitydefs.name2codepoint[ent])
    try:
        return _UNESCAPE.sub(fixup,s)
    except:
        print "unescape failed: %s" % repr(s)
        raise

class UnknownVariable(Exception):
    pass

class UnsupportedVariableExpression(Exception):
    pass

def replace_vars(m):
    """ Replace vars in 'content' portion.
    :m: match object
    :returns: string"""
    var = m.group(1)
    default = m.group(2)

    if not re.match(r'\w+$', var):
        raise UnsupportedVariableExpression(var)

    translate_vars = {
            'TM_PHP_OPEN_TAG_WITH_ECHO': 'g:UltiSnipsOpenTagWithEcho',
            'TM_PHP_OPEN_TAG': 'g:UltiSnipsOpenTag',
            'PHPDOC_AUTHOR': 'g:snips_author',
            }
    # TODO: TM_SELECTED_TEXT/([\t ]*).*/$1/m

    if var in translate_vars:
        newvar = translate_vars[var]
    else:
        # TODO: this could be autogenerated
        raise UnknownVariable(var)

    return "`!v exists('%s') ? %s : '%s'`" % (newvar, newvar, default)

def parse_content(c):
    try:
        data = ElementTree.fromstring(c)[0]

        rv = {}
        for k,v in zip(data[::2], data[1::2]):
            rv[k.text] = unescape(v.text)

        if re.search( r'\$\{\D', rv["content"] ):
            rv["content"] = re.sub(r'\$\{([^\d}][^}:]*)(?::([^}]*))?\}', replace_vars, rv["content"])

        return rv
    except (ExpatError, ElementTree.ParseError) as detail:
        print "   Syntax Error: %s" % (detail,)
        print c
        return None
    except UnknownVariable as detail:
        print "   Unknown variable: %s" % (detail,)
        return None
    except UnsupportedVariableExpression as detail:
        print "   Unsupported variable expression: %s" % (detail,)
        return None

def fetch_snippets_from_svn(name):
    base_url = "http://svn.textmate.org/trunk/Bundles/" + name + ".tmbundle/"
    snippet_idx = base_url + "Snippets/"

    idx_list = urllib.urlopen(snippet_idx).read()


    rv = []
    for link in re.findall("<li>(.*?)</li>", idx_list):
        m = re.match(r'<a\s*href="(.*)"\s*>(.*)</a>', link)
        link, name = m.groups()
        if name == "..":
            continue

        name = unescape(name.rsplit('.', 1)[0]) # remove Extension
        print "Fetching data for Snippet '%s'" % name
        content = urllib.urlopen(snippet_idx + link).read()

        cont = parse_content(content)
        if cont:
            rv.append((name, cont))

    return rv

def fetch_snippets_from_dir(path):
    """ Fetch snippets from a given path"""

    rv = []
    for filename in glob.glob(os.path.join(path, '*.tmSnippet')):
        print "Reading file %s" % filename
        f = open(filename)
        content = f.read()

        cont = parse_content(content)
        if cont:
            name = os.path.splitext(os.path.basename(filename))[0]
            rv.append((name, cont))
    return rv

def write_snippets(snip_descr, f):

    for name, d in snip_descr:
        if "tabTrigger" not in d:
            continue

        if "content" not in d or d["content"] is None:
            print "SKIP: %s (no content)" % (d,)
            continue

        f.write('snippet %s "%s"\n' % (d["tabTrigger"], name))
        f.write(d["content"].encode("utf-8") + "\n")
        f.write("endsnippet\n\n")



if __name__ == '__main__':
    import sys

    bundle = sys.argv[1]

    if os.path.isdir(bundle):
        name = sys.argv[2]
        rv = fetch_snippets_from_dir(bundle)
    else:
        rv = fetch_snippets_from_svn(bundle)
        name = bundle.lower()

    write_snippets(rv, open("tm_" + name + ".snippets","w"))

