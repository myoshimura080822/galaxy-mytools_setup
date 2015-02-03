# galaxy-mytools_setup

====

## Overview
BiT Workflow(RNA seq for eXpress,Sailfish + DEG(edgeR))実行環境のセットアップスクリプト群

*1. install_toolshed_tools.py*  

- main ToolShedで公開されているツールをAPI経由でインストールする  

*2. setup_sailfish_in_Galaxy.py*  

- sailfish indexをGalaxy環境に作成する

*3. bit-tools_install.py*  

- BiT Workflowに必要なカスタムツールをDL, Galaxyに配置する  

*4. bit-workflow_install.py*  

- BiT WorkflowをAPI経由でインポートする

## Description
*1. install_toolshed_tools.py*  

- yamlに定義されたツールを一括でインストールする。
	- 一度でも手動で削除した場合、Galaxyは「すでにインストールされたツール」とみなすので注意
	- その場合は手動で再インストールする必要があります

*2. setup_sailfish_in_Galaxy.py*  

- sailfish indexをGalaxy環境に作成する
- 現在は以下の4つが追加されます
	- human/Ensembl hg19 (GRCh37.75 cdna_all)
	- human/Ensembl hg38 (GRCh38 cdna_all)
	- mouse/Ensembl mm9 (NCBIM37.67 cdna_all)
	- mouse/Ensembl mm10 (GRCm38 cdna_all)
- 新たにindexを追加したい場合
	- index_file_list.txtにカンマ区切りで「id,DLアドレス,表示名」を追記する
- xmlを変更するので、Galaxyの再起動が必要です

*3. bit-tools_install.py*  

- Githubからカスタムツールを一括でDLし、配置する
	- /usr/local/galaxy4/galaxy-dist/tools/ 配下にすでに"galaxy-mytools_rnaseq" がある場合は削除かrenameが必要です
- xmlを変更するので、Galaxyの再起動が必要です

*4. bit-workflow_install.py*  

- GithubからBiT Workflowを一括でDLし、配置する
	- /usr/local/galaxy4/galaxy-dist/tools/ 配下にすでに"galaxy-workflow_rnaseq" がある場合は削除かrenameが必要です

## Requirement

* Galaxy API_KEY

