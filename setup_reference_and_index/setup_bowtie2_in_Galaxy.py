# -*- coding: utf-8 -*-
import sys, traceback
import os
import shutil
import time
import subprocess
from subprocess import check_call
import codecs
from xml.etree import ElementTree as ET
from git import Repo
import ftplib

print 'python version:' + sys.version
print 'create & setting bowtie2-index Started......'

argvs = sys.argv
argc = len(argvs)

if (argc != 3):
    print 'Usage: # python %s filename(index_list) galaxy-username' % argvs[0]
    quit()

homedir = '/usr/local/' + argvs[2]
bit_dname = homedir + '/bit_tools'
out_dname = bit_dname + '/bowtie2_index'
dist_dname = homedir + '/galaxy-dist'
loc_dname = dist_dname + '/tool-data'
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

def makeDir(dname):
    if os.path.exists(dname) is False:
        os.mkdir(dname)
        print '%s (dir) created.' % dname
    else:
        print '%s (dir) is already exists.' % dname

def print_tree(directory):
    for root, dirs, files in os.walk(directory):
        #yield root
        for file in files:
            yield os.path.join(root, file)

def create_dl_list(index_list):
    ret = []
    for item in index_list:
        list = item.split(',')
        item_dir = out_dname + '/' + list[0]
        makeDir(item_dir)
        dl_path = item_dir + '/' + list[1].split('/')[-1]
        print 'downloading-file: ' + dl_path
        if os.path.isfile(dl_path):
            print '>>>>>>>>>> This file is already exists. continue next.'
            continue
        ret.append(list[1])
    return ret

def ftp_download(url, index_list):

    listitem = filter(lambda x:x.find(url.split('/')[-1].split('.')[0]) > -1, index_list)
    print listitem
    if len(listitem) > 0:
        os.chdir(out_dname + '/' + listitem[0].split(',')[0])
        print 'current dir is %s' % os.getcwd()
    else:
        print 'download dir is not found. %s' % out_dname + '/' + listitem[0].split(',')[0] 
        os.chdir(out_dname)
        
    dlinfo = url.split('/')
    print dlinfo
    login_name = ""
    login_pass = ""
    if '@' in dlinfo[2]:
        hostname = dlinfo[2].split("@")[-1]
        login_name = dlinfo[2].split("@")[0].split(":")[0]
        login_pass = dlinfo[2].split("@")[0].split(":")[1]
    else:
        hostname = dlinfo[2]

    dirname = "/".join(dlinfo[3:-1])
    filename = dlinfo[-1]
    print hostname + ':' + dirname + ':' + filename
    print "login_name/pass : " + login_name + "/" + login_pass
    
    ftp=ftplib.FTP(hostname)
    
    if not login_name == "":
        ftp.login(login_name, login_pass)
    else:
        ftp.login()

    ftp.set_debuglevel(1)
    ftp.set_pasv(True)
    ftp.cwd(dirname + '/')
    print('PWD:' + ftp.pwd())
    fileList = ftp.nlst();
    print('NLST:' + str(fileList))
    ftp.retrbinary("RETR " + filename, open(filename, 'wb').write)
    print('DOWNLOAD COMPLETE')
    ftp.quit()

def get_bowtie2index_dir(path):
    dir_list = []
    for (root, dirs, files) in os.walk(path):
        for dir in dirs:
            dir_list.append( os.path.join(root,dir).replace("\\", "/") )
    
    dir_chk = filter(lambda x:x.find("Bowtie2Index") > -1, dir_list)
    return dir_chk[0] if len(dir_chk) > 0 else ""

def unpack_and_make_filelist(item, input_index_list):
    index_name = out_dname + '/' + item.split(',')[0]
    os.chdir(index_name)
    dir_chk = get_bowtie2index_dir(os.getcwd())
    print dir_chk 
    if len(dir_chk) > 0:
        print "%s bowtie-index is already downloaded." % index_name
    else:
        
        for filename in print_tree(os.getcwd()):
            print filename
            ext = ".".join(filename.split('.')[1:])
            print ext
            if ext == 'tar.gz':
                subprocess.check_call(["tar","-zxvf", filename])

    
    listchk = [index_name in x for x in input_index_list]
    if len(listchk) > 0:
        return get_bowtie2index_dir(os.getcwd())
    else:
        return ""

def create_loc_file(index_dir, index_list):
    f = codecs.open("bowtie2_indices.loc", "w", "utf-8")
    for dir_name in index_dir:
        if len(dir_name) > 0:
            item_info = filter(lambda x:x.find(dir_name.split('/')[-6]) > -1, index_list)[0]
            index_id = item_info.split(',')[0]
            index_name = item_info.split(',')[2]
            str_loc = '%s : %s : %s : %s' % (index_id,index_id,index_name,dir_name + '/genome')
            print str_loc
            f.write('%s\t%s\t%s\t%s\n' % (index_id,index_id,index_name,dir_name + '/genome'))
    f.close()

def add_tool_data_table_conf(tree):
    root_elm = tree.getroot()
    add_node = ET.Element('table', name='tophat2_indexes', comment_char='#')
    snode_col = ET.Element('columns')
    snode_col.text = 'value, dbkey, name, path'
    snode_file = ET.Element('file', path='tool-data/bowtie2_indices.loc')
    add_node.append(snode_col)
    add_node.append(snode_file)
    root_elm.append(add_node)
    print root_elm.getchildren()[len(root_elm)-1].attrib
    print root_elm.getchildren()[len(root_elm)-1].getchildren()
    tree.write('tool_data_table_conf.xml')

def main():
    try:
        input_index_list = []
        input_index_list = read_input()
        print 'length of index_list: ' + str(len(input_index_list))
        
        makeDir(bit_dname)
        makeDir(out_dname)

        print ':::::::::::::::::::::::::::::::::::::::::::'
        print '>>>>>>>>>>>>>>>>> download bowtie2 index-files ...'
        dl_url_list = []
        dl_url_list = create_dl_list(input_index_list)
        
        if len(dl_url_list) > 0:
            print 'start downloading...'
            for url in dl_url_list:
                ftp_download(url, input_index_list)
        else:
            print 'no execute download task.'
        
        print ':::::::::::::::::::::::::::::::::::::::::::'
        print '>>>>>>>>>>>>>>>>> unpacking and make-list bowtie2 index-files...'
        index_dir = [unpack_and_make_filelist(item, input_index_list) for item in input_index_list]
        print index_dir

        print ':::::::::::::::::::::::::::::::::::::::::::'
        print '>>>>>>>>>>>>>>>>> create bowtie2_indices.loc...'
        os.chdir(loc_dname)
        create_loc_file(index_dir, input_index_list)

        print ':::::::::::::::::::::::::::::::::::::::::::'
        print '>>>>>>>>>>>>>>>>> add tophat2 index-node to tool_data_table_conf.xml...'
        os.chdir(dist_dname)
        tree = ET.parse('tool_data_table_conf.xml')

        tophat2_node = 0
        for e in tree.getiterator():
            if e.get('name') == 'tophat2_indexes':
                tophat2_node = 1

        if tophat2_node == 0:
            add_tool_data_table_conf(tree)
        else:
            print 'tophat2 index-node already created.'

        print ':::::::::::::::::::::::::::::::::::::::::::'
        print '>>>>>>>>>>>>>>>>> script ended :)'

    except KeyboardInterrupt:
        print ">>>>>>>>>>>>>>>>> Caught KeyboardInterrupt. Terminating workers..."
        sys.exit(1)
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
