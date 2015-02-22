#!/bin/sh

if [ $# -ne 2 ]; then
    echo "Invalid argument. (require Reference fastq_Dir and downsize(ex:1/10 -> 10))" 1>&2
    exit 1
fi

if [ ! -f ./listQuartz.txt ]; then
    echo "listQuartz.txt not found." 1>&2
    exit 1
fi

if [ ! -d $1 ]; then
    echo "$1 Dir not found." 1>&2
    exit 1
fi

expr "$2" + 1 >/dev/null 2>&1
if [ ! $? -lt 2 ]; then
    echo "downsize is not Numeric."
    exit 1
fi

if [ ! -d ./log ]; then
    mkdir log
fi

div_name=div$2
sub_value=`python -c "print round(1/float($2),4)"`
output_dir=$div_name'_output'
#echo $output_dir;echo $sub_value

ref_path="$1"
ref_path_es=`echo $ref_path | sed s,/,\\\\\\\\/,g`
#echo $ref_path_es

# output logDir
DATE=`date '+%F_%R'`
LOGFILE=./log/$DATE.log

{
    echo "***** [$0] start " `date +'%Y/%m/%d %H:%M:%S'` " *****"
    echo ""
    echo "[" `date +'%Y/%m/%d %H:%M:%S'` "] read fastq file list....."

    Quartz=()
    while read line
    do
        Quartz=(${Quartz[@]} ${line})
        echo ${line}
    done <./listQuartz.txt

    countSamples=${#Quartz[@]}

    echo "[" `date +'%Y/%m/%d %H:%M:%S'` "] exec down sampling....."

    rm -rf $output_dir
    mkdir $output_dir

    for((i=0;i<$countSamples;i++))
    do
        call=`expr $i + 1`
        echo""
        echo "$call / $countSamples of list files (QuartzID : ${Quartz[$i]})"
        echo make shell script Down_${Quartz[$i]}.sh start...
        
        sed -e "s/REFNAME/$ref_path_es\/${Quartz[$i]}/g;s/OUTNAME/$output_dir\/${Quartz[$i]}_$div_name/g;s/SUBVALUE/$sub_value/g" ./sh_templates/down_quartz_template > Down_${Quartz[$i]}.sh

        echo make shell script Down_${Quartz[$i]}.sh end...
        chmod +x Down_${Quartz[$i]}.sh | echo chmod Down_${Quartz[$i]}.sh
        sh Down_${Quartz[$i]}.sh
        rm Down_${Quartz[$i]}.sh | echo rm Down_${Quartz[$i]}.sh
    done
    echo ""
    echo "***** [$0] end " `date +'%Y/%m/%d %H:%M:%S'` " *****"

} >> "$LOGFILE" 2>&1

