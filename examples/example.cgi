#!/usr/bin/python -tt
#
import sys
import cgi
import cgitb
cgitb.enable()

import json
import urllib2

def cgimain():
    # Read location of the json file from a config file
    fh = open('config.txt')
    remote = fh.read()
    fh.close()
    remote = remote.strip()

    # GET the latest contents
    response = urllib2.urlopen(remote)
    contents = response.read()
    response.close()
    reldata = json.loads(contents)

    # Output latest stable kernel version
    output = ("Latest stable kernel: %s\n" %
        reldata['latest_stable']['version'])
    sys.stdout.write('Status: 200 OK\n')
    sys.stdout.write('Content-type: text/plain\n')
    sys.stdout.write('Content-Length: %s\n' % len(output))
    sys.stdout.write('\n')

    sys.stdout.write(output)


if __name__ == '__main__':
    cgimain()

