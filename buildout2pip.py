#!/usr/bin/env python
# Takes a buildout.cfg file and converts it to a pip-compatible format
# Created by Hany Fahim <hany@vmfarms.com>
# Copyright 2012 VM Farms Inc.

import os
import sys
import ConfigParser


def main():
    try:
        buildoutcfg = sys.argv[1]
    except:
        buildoutcfg = "buildout.cfg"
    convert(buildoutcfg, sys.stdout)


def convert(buildoutcfg, piprequirement):
    config = ConfigParser.RawConfigParser()
    config.optionxform = str  # Package names are case-sensitive
    config.read([buildoutcfg])

    # We only support one level of nesting, but this is enough
    # to use an autmatically updated versions file
    try:
        extended = config.get('buildout', 'extends')
    except ConfigParser.NoOptionError:
        extended = None
    if extended:
        extended = os.path.join(os.path.dirname(buildoutcfg), extended)
        config.read([buildoutcfg, extended])

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
            piprequirement.write(eggs[egg] + "\n")
        elif eggs[egg] == '':
            piprequirement.write(egg + "\n")
        else:
            piprequirement.write("%s==%s\n" % (egg, eggs[egg]))

if __name__ == "__main__":
    main()
