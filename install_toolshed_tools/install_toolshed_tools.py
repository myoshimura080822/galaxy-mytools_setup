# -*- coding: utf-8 -*-
import sys,traceback
import os
import yaml
import datetime as dt
import bioblend
from bioblend.galaxy import GalaxyInstance
from bioblend.galaxy.toolshed import ToolShedClient
from bioblend.toolshed import ToolShedInstance
print "python :" + sys.version

print u"install_toolshed_tools.py Started......"

argvs = sys.argv
argc = len(argvs)

if (argc != 2):
    print 'Usage: # python %s "<APY_KEY>"' % argvs[0]
    quit()

#============== Galaxy in 172.18.70.161 ================
GALAXY_URL = 'http://127.0.0.1:8080/'
API_KEY = argvs[1]
print API_KEY

def main():
    try:
        tool_list_file = 'tool_shed_tool_list.yaml'
        # Load tool list
        with open(tool_list_file, 'r') as f:
            tl = yaml.load(f)

        r_info = tl['tools']
        responses = []
        counter = 1
        total_num_tools = len(r_info)
        default_err_msg = 'All repositories that you are attempting to install have been previously installed.'

        gInstance = GalaxyInstance(url = GALAXY_URL, key=API_KEY)
        tsc = ToolShedClient(gInstance)
        tool_set = tsc.get_repositories()
        tool_name_list = [x['name'] for x in tool_set]

        for r in r_info:

            #if r['name'] in tool_name_list:
            #    print '%s already installed. skipping...' % r['name']
            #    continue

            if 'install_tool_dependencies' not in r:
                r['install_tool_dependencies'] = True
            if 'install_repository_dependencies' not in r:
                r['install_repository_dependencies'] = True
            if 'tool_shed_url' not in r:
                r['tool_shed_url'] = 'http://toolshed.g2.bx.psu.edu'

            ts = ToolShedInstance(url=r['tool_shed_url'])

            if 'revision' not in r:
                r['revision'] = ts.repositories.get_ordered_installable_revisions(r['name'], r['owner'])[-1]

            start = dt.datetime.now()
            print '\n(%s/%s) Installing tool %s from %s to section %s' % (counter, total_num_tools, r['name'], r['owner'], r['tool_panel_section_id'])

            try:
                response = tsc.install_repository_revision(r['tool_shed_url'], r['name'], r['owner'], r['revision'], r['install_tool_dependencies'], r['install_repository_dependencies'], r['tool_panel_section_id'])
            # new_tool_panel_section_label='API tests')
            except:
                print 'failed installing %s tool.' % r['name']
                info = sys.exc_info()
                err_msg = '>>>>>> This tool already installed in Galaxy.' if '"err_code": 400008' in str(info[1]) else str(info[1] )
                print err_msg
            else:
                print 'successful %s installation.' % r['name']
            end = dt.datetime.now()

            counter += 1

        # print responses
        print "\r\nAll tools listed in %s have been installed." % tool_list_file

    except:
        info = sys.exc_info()
        tbinfo = traceback.format_tb( info[2] )
        print 'Error Info...'.ljust( 80, '=' )
        for tbi in tbinfo:
            print tbi
        print '  %s' % str( info[1] )
        print '\n'.rjust( 85, '=' )
        sys.exit(1)

if __name__ == '__main__':
    main()
