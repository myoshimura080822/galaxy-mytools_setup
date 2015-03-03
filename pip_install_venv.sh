#!/bin/bash
{
    echo $1
    . $1
    pip list
    pip install python-dateutil
    pip install pandas
    pip install bioblend
    pip list

} 2>&1
