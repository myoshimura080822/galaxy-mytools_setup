# -*- coding: utf-8 -*-
import sys, traceback
import os
from git import Repo
import bioblend
from bioblend.galaxy import GalaxyInstance
from bioblend.galaxy.workflows import WorkflowClient

print 'bit-workflow_install.py Started......'

GALAXY_URL = 'http://127.0.0.1:8080/'
API_KEY = '5192626488c47dab7a8747861f345a54'

dist_dname = '/usr/local/galaxy4/galaxy-dist'
wf_dname = '/usr/local/galaxy4/galaxy-dist/workflow_file'

def get_all_ga(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            name, ext = os.path.splitext(file)
            if not '.git' in root and ext == '.ga':
                yield os.path.join(root, file)

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
        print '>>>>>>>>>>>>>>>>> clone BiT Tools from github...'
        if not os.path.exists(wf_dname + '/galaxy-workflow-rnaseq'):
            os.chdir(wf_dname)
            git_url = 'https://github.com/myoshimura080822/galaxy-workflow-rnaseq.git'
            Repo.clone_from(git_url, 'galaxy-workflow-rnaseq')
        else:
            print 'BiT Workflow already cloned. To update, Please delete, move or rename "/galaxy-workflow-rnaseq" before script execute.'
            #return 0

        print ':::::::::::::::::::::::::::::::::::::::::::'
        print '>>>>>>>>>>>>>>>>> delete and inport workflow files...'

        mytoolsdir = wf_dname + '/galaxy-workflow-rnaseq/'
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

