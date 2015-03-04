# galaxy-mytools_setup

====

## Overview
Setup ENV for Execute BiT-Workflow (RNA seq + DEG)

###*1. downsize_fastq_script(Dir)* 

- downsize fastq-files.

	- `/downsize_fastq.sh`

		- use: `$sh downsize_fastq.sh <fastq_dir-path> <downsize(ex:1/10 = 10)>`
	
	- `/listQuartz.txt`

		- to define the list of file to downsize（not need ".fastq"）

###*2. install_toolshed_tools(Dir)*

- install stable toolShed-Tools to Galaxy. 

	- `/install_toolshed_tools.py`

		- use: `python install_toolshed_tools.py <galaxy username(admin)>`

	- `/tool_shed_tool_list.yaml`

		- to define a list of tools and their versions that will be installed as Galaxy.

###*3. setup_reference_and_index(Dir)* 

- create sailfish index and transcriptome.fa setting for RNA-seq to be used Galaxy. 

- Requirement: Galaxy Master API_KEY (setting ini)

	- `/setup_TranscriptomeRef_in_Galaxy.py`

		- use: `python setup_TranscriptomeRef_in_Galaxy.py <Ref file_list.txt> <galaxy username(admin)>`

	- `/setup_sailfish_in_Galaxy.py`

		- use: `python setup_sailfish_in_Galaxy.py <Ref file_list.txt> <galaxy username(admin)>`

	- `/index_file_list.txt`

		- to define a list of Reference Seqence files information.

###*4. bit-tools_install.py*  

- clone, install and setting BiT custom-tools.

- Requirement: remove, move or rename dir "..galaxy_dist/tools/galaxy-mytools_rnaseq" before script execute.

- use: `python bit-tools_install.py <galaxy username(admin)>`

*4. bit-workflow_install.py*  

- clone, install and setting BiT custom-WFs.

- Requirement: remove, move or rename dir "..galaxy_dist/workflow_file/galaxy-workflow_rnaseq" before script execute.

- use: `python bit-tools_install.py <galaxy username(admin)>`

