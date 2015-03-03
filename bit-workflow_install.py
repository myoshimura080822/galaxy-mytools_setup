# -*- coding: utf-8 -*-
import sys, traceback
import os
from git import Repo
from ConfigParser import SafeConfigParser
import bioblend
from bioblend.galaxy import GalaxyInstance
from bioblend.galaxy.workflows import WorkflowClient

print 'bit-workflow_install.py Started......'

argvs = sys.argv
argc = len(argvs)

if (argc != 3):
    print 'Usage: # python %s USER_API_KEY galaxy-username' % argvs[0]
    quit()

homedir = '/usr/local/' + argvs[2]
dist_dname = homedir + '/galaxy-dist'
wf_dname = dist_dname + '/workflow_file'

GALAXY_URL = 'http://127.0.0.1:8080/'
conf = SafeConfigParser()
conf.read(dist_dname + '/universe_wsgi.ini')
#API_KEY = unicode(conf.get("app:main","master_api_key"))
API_KEY=str(argvs[1])
if (len(API_KEY) == 0):
    print 'No setting galaxy MasterAPI_KEY.'
    quit()
else:
    print 'API_KEY: ' + API_KEY

def get_all_ga(directory):
    ret = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            name, ext = os.path.splitext(file)
            if not '.git' in root and ext == '.ga':
                ret.append(os.path.join(root, file))
    return ret

def makeDir(dname):
    if os.path.exists(dname) is False:
        os.mkdir(dname)
        print '%s (dir) created.' % dname
    else:
        print '%s (dir) is already exists.' % dname

def main():
    try:
        gInstance = GalaxyInstance(url = GALAXY_URL, key=API_KEY)
        wClient = WorkflowClient(gInstance)

        print ':::::::::::::::::::::::::::::::::::::::::::'
        print '>>>>>>>>>>>>>>>>> get current workflowlist...'
        gInstance = GalaxyInstance(url = GALAXY_URL, key=API_KEY)
        wClient = WorkflowClient(gInstance)
        dataset = wClient.get_workflows()
        wf_namelist = [x['name'] for x in dataset if x['deleted'] == False]
        print wf_namelist
        print ':::::::::::::::::::::::::::::::::::::::::::'
        print '>>>>>>>>>>>>>>>>> clone BiT Workflows from github...'
        if not os.path.exists(wf_dname + '/galaxy-workflow_rnaseq'):
            makeDir(wf_dname)
            os.chdir(wf_dname)
            git_url = 'https://github.com/myoshimura080822/galaxy-workflow_rnaseq.git'
            Repo.clone_from(git_url, 'galaxy-workflow_rnaseq')
        else:
            print 'BiT Workflow already cloned. To update, Please delete, move or rename "/galaxy-workflow_rnaseq" before script execute.'
            return 0

        print ':::::::::::::::::::::::::::::::::::::::::::'
        print '>>>>>>>>>>>>>>>>> delete and inport workflow files...'

        mytoolsdir = wf_dname + '/galaxy-workflow_rnaseq/'
        clone_wf_list = [file.replace(mytoolsdir, "") for file in get_all_ga(mytoolsdir)]
        print clone_wf_list
        delete_itm =[]
        [[ delete_itm.append(y) for y in wf_namelist if y.find(x.replace('.ga','')) > -1] for x in clone_wf_list]
        print delete_itm
        id_list = []
        [[id_list.append(x['id']) for x in dataset if x['name'].find(y) > -1] for y in delete_itm]
        print id_list
        [wClient.delete_workflow(x) for x in id_list]
        print wClient.get_workflows()
        [wClient.import_workflow_from_local_path(file) for file in get_all_ga(mytoolsdir)]
        print wClient.get_workflows()

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

