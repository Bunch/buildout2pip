#!/usr/bin/env python
# Takes a buildout.cfg file and converts it to a pip-compatible format
# Created by Hany Fahim <hany@vmfarms.com>
# Copyright 2012 VM Farms Inc.

import sys
import ConfigParser


def main():
    try:
        buildoutcfg = sys.argv[1]
    except:
        buildoutcfg = "buildout.cfg"
    convert(buildoutcfg)


def convert(buildoutcfg):
    config = ConfigParser.ConfigParser()
    config.read(buildoutcfg)

    # First get list of eggs
    temp_eggs = config.get('eggs', 'eggs').split('\n')
    eggs = {}
    # clean up comments
    for egg in temp_eggs:
        eggs[egg.split()[0]] = ''

    # Next need to match with versions
    for egg, version in config.items('versions'):
        if egg in eggs:
            eggs[egg] = version

    # Next we need to incorporate sources
    for egg, source in config.items('sources'):
        if egg in eggs:
            options = None
            (rcs, url) = source.split(None, 1)
            # account for extra options
            try:
                (url, options) = url.split()
            except ValueError:
                pass

            # Format the URL properly
            if url.startswith('git@'):
                # git@github.com:MyProject/project.git
                # git+ssh://git@myproject.org/MyProject/#egg=MyProject
                (userhost, uri) = url.split(':')
                url = "git+ssh://%s/%s" % (userhost, uri)
            elif url.startswith('http'):
                url = "git+%s" % url

            if options:
                (key, val) = options.split('=')
                if key in ['rev', 'branch']:
                    eggs[egg] = "-e %s@%s#egg=%s" % (url, val, egg)
                else:
                    print "Unknown option found: %s" % key
            else:
                eggs[egg] = "-e %s#egg=%s" % (url, egg)

    # Putting it all together
    for egg in eggs:
        if eggs[egg].startswith('-e'):
            print eggs[egg]
        elif eggs[egg] == '':
            print egg
        else:
            print "%s==%s" % (egg, eggs[egg])

if __name__ == "__main__":
    main()
