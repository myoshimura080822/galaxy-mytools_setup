# -*- coding: utf-8 -*-
import sys, traceback
import os
import shutil
import requests
import time
import grequests
import itertools
from itertools import product
print "python :" + sys.version

argvs = sys.argv
argc = len(argvs)

print argvs[0] + ' Started.....'

if (argc != 3):
    print 'Usage: # python %s filename(file_list) galaxy-username' % argvs[0]
    quit()

homedir = '/usr/local/' + argvs[2]
out_dname = homedir + '/transcriptome_ref'

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

def create_dl_list(ref_list):
    ret = []
    for item in ref_list:
        item_list = item.split(',')
        dl_path = item_list[1]
        dl_item = item_list[1].split('/')[-1]
        print 'downloading-file: ' + dl_path
        if os.path.isfile(dl_item.replace('.gz', '')):
            print '>>>>>>>>>> This Ref-file is already exists. continue next.'
            continue
        ret.append(item_list[1])
    return ret

def grequests_async(dl_list, ref_list):
    rs = (grequests.get(url) for url in dl_list)
    for r in grequests.map(rs):
        print r.url + ' >>>>>>>>>><Response>' + str(r.status_code)

        out_listitem = next(itertools.ifilter(lambda x:x.find(str(r.url)) > -1, ref_list), None)
        print out_listitem

        file_name = str(r.url).split('/')[-1]
        #out_dir = out_dname + '/' + out_listitem.split(',')[0]
        if os.path.isfile(out_dname + '/' + file_name):
            print '%s is already exists.' % out_dname + '/' + file_name
        else:
            print 'creat-file in ' + out_dname
            f = open(file_name, 'w')
            f.write(r.content)
            f.close

def unpack_files():
    index_files = []
    for file in print_tree(out_dname):
        root, ext = os.path.splitext(file)
        if ext == '.gz':
            subprocess.check_call(["gunzip","-fd",file])
            index_files.append(file)
        elif ext == '.fa':
            index_files.append(file)
            index_files = sorted(set(index_files), key=index_files.index)
    return index_files



def main():
    try:
        ref_list = []
        ref_list = read_input()
        print 'length of ref_list: ' + str(len(ref_list))

        makeDir(out_dname)
        os.chdir(out_dname)
        print 'moved to %s' % os.getcwd()

        print ':::::::::::::::::::::::::::::::::::::::::::'
        print '>>>>>>>>>>>>>>>>> download transcritome files ...'

        dl_url_list = []
        dl_url_list = create_dl_list(ref_list)

        if len(dl_url_list) > 0:
            print 'start download-jobs...'
            grequests_async(dl_url_list, ref_list)
            print 'all download-jobs finished.'
        else:
            print 'no execute download-jobs.'

        print ':::::::::::::::::::::::::::::::::::::::::::'
        print '>>>>>>>>>>>>>>>>> unpacking transcritome files...'
        ref_files = []
        ref_files = unpack_files()
        print 'Ref-files in current dir: ' + ref_files


        # Load tool list
        with open(tool_list_file, 'r') as f:
            tl = yaml.load(f)

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
