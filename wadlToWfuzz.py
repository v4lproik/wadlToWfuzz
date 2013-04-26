#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Small python script in order to be able to extract the different methods of an application.wadl file and then
get the url ready to be passed as an argument to wfuzz
'''

__author__ = "v4lproik"
__date__ = "26/04/2013"
__version__ = "1.0"
__maintainer__ = "v4lproik"
__email__ = "v4lproik@gmail.com"
__status__ = "Production"

try:
    import requests
    import array
    import lxml.etree as XML
    import re
    import traceback
    import sys
    import urlparse
    import ConfigParser
    import argparse
except ImportError, err:
    raise
    print >>sys.stderr, "[X] Unable to import : %s\n" % err
    sys.exit(1)

def banner():
    banner = '''
    |----------------------------------------------------------|
    |                 Extract WADL to Wfuzz 1.0                |
    |                           V4lproik                       |
    |----------------------------------------------------------|\n'''
    print banner

def checkArgs():
    if len(sys.argv) < 4:
        parser.print_help()
        sys.exit()

def extract(element, elt_resource, elt_method, root_path=''):
    child_resources = element.findall(elt_resource)
    this_methods = element.findall(elt_method)

    this_path = str(element.get('path'))

    if not this_path.startswith('/') and not root_path.endswith('/'):
        this_path = '/' + this_path

    if this_methods:
        resources.append([
            {
                'path': this_path,
                'type': method.get('name'),
                'id': method.get('id')
            }
            for method in this_methods])

    for el in child_resources:
        extract(el, elt_resource, elt_method, root_path=this_path)

def parse(filename):
    tree = XML.parse(filename)
    root = tree.getroot()
    ns = root.nsmap[None]

    
    elt_resources = root.find(u'{%s}resources' % ns)
    elt_resource = u'{%s}resource' % ns
    elt_method = u'{%s}method' % ns
    value = [elt_resources, elt_resource, elt_method]

    return value

def save_file(filename, base_url):
    file = open(filename, 'w')
    if not base_url.endswith('/'):
        base_url = base_url + '/'
    r = requests.get(base_url + filename)
    file.write(r.text)
    file.close()

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        gr1 = parser.add_argument_group("main arguments")
        gr1.add_argument('-d', '--domain', dest='domain', required=True, help='Domain to check')
        gr1.add_argument('-f', '--filename', dest='filename', required=True, default="application.wadl", help='default : application.wadl')
        gr1.add_argument('-w', '--wfuzz', dest='wfuzz', default=False, action='store_true', help='wizzard for wfuzz url')

        checkArgs()

        args = parser.parse_args()

        resources = []

        base_url = args.domain
        
        banner()
        save_file(args.filename, base_url)
        value = parse(args.filename) 
        extract(value[0], value[1], value[2])

        for resource in resources:
            for res in resource:
                print "Method " + res['id'] + " uses " + res['type'] + ":"
                if res['path'].startswith('/') and base_url.endswith('/'):
                    res['path'] = res['path'][1:]
                print base_url + res['path']
                print ""
                
                if (args.wfuzz):
                    url_fuzz = base_url + res['path']
                    count = 0
                    for res in re.findall('{(.*?)}', res['path']):
                        if(args.wfuzz):
                            response = raw_input("Enter a value for the variable " + res + ": ")
                            if(response==""):
                                count += 1
                                if(count==1):
                                    response = "FUZZ"
                                else:
                                    response = "FUZ"+str(count)+"Z"
                            url_fuzz = url_fuzz.replace("{"+res+"}", response, 1)
                    print "Fuzz URL : " + url_fuzz
                    print ""
    except KeyboardInterrupt:
        print "Process interrupted by user.."
    except:
        print "\n\n", traceback.format_exc()

