# -*- coding: utf-8 -*-
import sys, traceback
import os
import ConfigParser
from git import Repo
from xml.etree import ElementTree as ET

print 'install_bit-tools.py Started......'

argvs = sys.argv
argc = len(argvs)

if (argc != 2):
    print 'Usage: # python %s galaxy-username' % argvs[0]
    quit()

homedir = '/usr/local/' + argvs[1]
dist_dname = homedir + '/galaxy-dist'
tool_dname = dist_dname + '/tools'

def read_input():
    f = open(argvs[1])
    ret_list = []

    for i in f.readlines():
        i = i.strip()
        if len(i) < 1:
            continue
        ret_list = ret_list + [i]

    f.close
    return ret_list

def add_tool_conf(tree, list):
    root_elm = tree.getroot()
    add_node = ET.Element('section', name='BiT Tools', id='bittools')
    for name in list:
        snode_tool = ET.Element('tool', file=name)
        add_node.append(snode_tool)
    root_elm.append(add_node)
    print root_elm.getchildren()[len(root_elm)-1].attrib
    print root_elm.getchildren()[len(root_elm)-1].getchildren()
    tree.write('tool_conf.xml')

def get_all_xml(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            name, ext = os.path.splitext(file)
            if not '.git' in root and ext == '.xml':
                yield os.path.join(root, file)

def main():
    try:
 #       input_tool_list = []
 #       input_tool_list = read_input()
 #       print 'length of tool_list: ' + str(len(input_tool_list))

        print ':::::::::::::::::::::::::::::::::::::::::::'
        print '>>>>>>>>>>>>>>>>> clone BiT Tools from github...'
        if not os.path.isfile(tool_dname + '/galaxy-mytools_rnaseq/Sailfish_custom/Sailfish_custom.xml'):
            os.chdir(tool_dname)
            git_url = 'https://github.com/myoshimura080822/galaxy-mytools_rnaseq.git'
            Repo.clone_from(git_url, 'galaxy-mytools_rnaseq')
        else:
            print 'BiT Tools already cloned. To update, Please delete, move or rename "/galaxy-mytools_rnaseq" before script execute.'
            return 0

        print ':::::::::::::::::::::::::::::::::::::::::::'
        print '>>>>>>>>>>>>>>>>> add BiT tool-node to tool_conf.xml...'

        mytoolsdir = tool_dname + '/galaxy-mytools_rnaseq/'
        xml_list = [file.replace(tool_dname + '/', "") for file in get_all_xml(mytoolsdir)]
        print (set(xml_list))
        print xml_list

        os.chdir(dist_dname)
        tool_tree = ET.parse('tool_conf.xml')
        sailfish_tool = 0
        for e in tool_tree.getiterator():
            if e.get('file') in xml_list:
                xml_list.remove(e.get('file'))
                print '%s tool node already created.' % e.get('file')
        print xml_list
        add_tool_conf(tool_tree, xml_list)

        print ':::::::::::::::::::::::::::::::::::::::::::'
        print '>>>>>>>>>>>>>>>>> script ended :)'
        return 0

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
    sys.exit(main())
