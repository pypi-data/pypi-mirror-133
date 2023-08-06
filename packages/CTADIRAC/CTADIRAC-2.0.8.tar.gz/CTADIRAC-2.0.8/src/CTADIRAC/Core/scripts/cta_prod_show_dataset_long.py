#!/usr/bin/env python

__RCSID__ = "$Id$"

import os

import DIRAC
from DIRAC import gLogger
from DIRAC.Core.Utilities.DIRACScript import DIRACScript as Script
from DIRAC.Core.Utilities.PrettyPrint import int_with_commas, printTable
from DIRAC.Resources.Catalog.FileCatalogClient import FileCatalogClient
from CTADIRAC.Core.Utilities.tool_box import read_lfns_from_file


def print_dataset_list(dataset_list):
  dataset_list.sort()
  print('\nAvailable datasets: %d\n' % len(dataset_list))
  for dataset_name in dataset_list:
    gLogger.notice(dataset_name)
  gLogger.notice('\n')


def get_list_of_datasets(tag=''):
  fc = FileCatalogClient()
  dataset_tag = '*%s*' % tag
  res = fc.getDatasets(dataset_tag)
  if not res['OK']:
    gLogger.error(res['Message'])
    DIRAC.exit(-1)
  dataset_dict = res['Value']
  dataset_list = list()
  for dataset_name in dataset_dict['Successful'][dataset_tag]:
    dataset_list.append(dataset_name)
  return dataset_list

def get_dataset_info(dataset_name):
  fc = FileCatalogClient()
  res = fc.getDatasetParameters(dataset_name)
  res = fc.getDatasets(dataset_name)
  if not res['OK']:
    gLogger.error("Failed to get datasets")
    DIRAC.exit(-1)
  dataset_dict = res['Value']
  res = dataset_dict['Successful'][dataset_name][dataset_name]
  number_of_files = res['NumberOfFiles']
  meta_query = res['MetaQuery']
  total_size = res['TotalSize']
  return (dataset_name, number_of_files, total_size, meta_query)
  
def print_dataset_storage_usage(dataset_name):

  fc = FileCatalogClient()
  fields = ["StorageElement", "Size", "Replicas"]
  name, n_files, size, mq = get_dataset_info(dataset_name)
  outputType = mq['outputType']
  result = fc.findDirectoriesByMetadata(mq)
  gLogger.notice('Directory size')
  for k, path in result['Value'].items():
    if os.path.basename(path) == outputType:
      gLogger.notice(path)
      result = fc.getDirectorySize(path,longOut=True)
      values = []
      if "PhysicalSize" in result["Value"]["Successful"][path]:
        totalSize = result["Value"]["Successful"][path]["PhysicalSize"]["TotalSize"]
        totalFiles = result["Value"]["Successful"][path]["PhysicalSize"]["TotalFiles"]
        for se, sdata in result["Value"]["Successful"][path]["PhysicalSize"].items():
          if not se.startswith("Total"):
            size = sdata["Size"]
            nfiles = sdata["Files"]
            values.append((se, int_with_commas(size), str(nfiles)))
        values.append(("Total", int_with_commas(totalSize), str(totalFiles)))
        printTable(fields, values)
 
def print_dataset_storage_usage_summary(path_list):

  fc = FileCatalogClient()
  fields = ["StorageElement", "Size", "Replicas"]
  values = []
  se_list = []
  stat_dict = {}
  total_stat_dict = {'Total':{'size':0,'nFiles':0}}

  # Initialize the list of SE for all paths
  for path in path_list:
    result = fc.getDirectorySize(path,longOut=True)
    if "PhysicalSize" in result["Value"]["Successful"][path]:
      for se, sdata in result["Value"]["Successful"][path]["PhysicalSize"].items():
        if not se.startswith("Total"):
          se_list.append(se)

  # Initialize the total_stat_dict with all SE keys        
  se_list = sorted(set(se_list))    
  for se in se_list:
    total_stat_dict.update({se:{'size':0,'nFiles':0}})

  # For each path get the directory usage and calculate the total usage for each SE
  # and the overall total usage 
  for path in path_list:
    result = fc.getDirectorySize(path,longOut=True)
    res_path_dict = result["Value"]["Successful"][path]
    if "PhysicalSize" in res_path_dict:
      if "TotalSize" in res_path_dict["PhysicalSize"]: 
        totalSize = res_path_dict["PhysicalSize"]["TotalSize"]
      if "TotalFiles" in res_path_dict["PhysicalSize"]:
        totalFiles = res_path_dict["PhysicalSize"]["TotalFiles"]
      for se, sdata in result["Value"]["Successful"][path]["PhysicalSize"].items():
        if not se.startswith("Total"):
          stat_dict.update({se:{'size': sdata["Size"],'nFiles':sdata["Files"]}})
      # Calculate the overall total usage    
      total_stat_dict['Total']['size'] += totalSize
      total_stat_dict['Total']['nFiles'] += totalFiles

    # Calculate the total usage for each SE  
    for se in stat_dict:
      total_stat_dict[se]['size'] +=  stat_dict[se]['size']
      total_stat_dict[se]['nFiles'] +=  stat_dict[se]['nFiles']
  
  # Update the values of the table for each SE
  for se in se_list:
    values.append((se, int_with_commas(total_stat_dict[se]['size']), str(total_stat_dict[se]['nFiles']))) 

  # Update the values of the table with the Total
  values.append(("Total", int_with_commas(total_stat_dict['Total']['size']), str(total_stat_dict['Total']['nFiles']))) 

  printTable(fields, values)
  

#########################################################
@Script()
def main():

  Script.setUsageMessage("""
Get statistics for datasets corresponding to the dataset name (may contain wild card)
if no dataset is specified it gives the list of available datasets
Usage:
   %s <datasetName or ascii file with a list of datasets> <options>

""" % Script.scriptName)
  
  Script.registerSwitch("l", "long", "print dataset details")
  Script.registerSwitch("", "SEUsage", "print storage usage summary per SE")
  switches, argss = Script.parseCommandLine(ignoreErrors=True)

  if len(argss) == 0:
    dataset_list = get_list_of_datasets()
    print_dataset_list(dataset_list)
    DIRAC.exit()
  elif len(argss) == 1:
    if os.path.isfile(argss[0]):
      gLogger.notice('Reading datasets from input file: %s' % argss[0])
      dataset_list = read_lfns_from_file(argss[0])
    else:
      dataset_name = argss[0]
      dataset_list = list()
      if dataset_name.find('*') > 0:
        dataset_list = get_list_of_datasets(dataset_name)
      else:
        dataset_list.append(dataset_name)
    print_dataset_list(dataset_list)

  long = False
  SEUsage = False
  for switch in switches:
    if 'l' == switch[0] or 'long' == switch[0]:
      long = True
    if 'SEUsage' == switch[0]:
      SEUsage = True
    
  if SEUsage:
    gLogger.notice('Getting statistics informations for all datasets\n')
    
  # Get dataset info only if SE usage report or dataset details are requested
  if SEUsage or long:
    path_list = []
    fc = FileCatalogClient()
    i=1
    for dataset_name in dataset_list:
      name, n_files, size, mq = get_dataset_info(dataset_name)
      if long:
        gLogger.notice('%d) Dataset name: %s' % (i, name))
        gLogger.notice('MetaQuery')
        gLogger.notice(str(mq))
        print_dataset_storage_usage(dataset_name)
        i+=1
      # Get the path list only if the SE usage report is requested  
      if SEUsage:  
        if 'outputType' in mq:
          outputType = mq['outputType']
        else:
          gLogger.error('Error: cannot get SEUsage for dataset %s' % name)
          gLogger.error('No outputType metadata defined')
          DIRAC.exit(-1)
        result = fc.findDirectoriesByMetadata(mq)
        for k, path in result['Value'].items():
          if os.path.basename(path) == outputType:
            path_list.append(path)

  if SEUsage:
    gLogger.notice('Storage usage for all datasets\n')
    print_dataset_storage_usage_summary(path_list)

  # To do: optimize to avoid calling twice get_dataset_info when using SEUsage or long options
  gLogger.notice('Summary table of all datasets')
  gLogger.notice('|_. Name |_. N files |_. Size(TB) |')
  total_size = 0.
  total_n_files = 0
  for dataset_name in dataset_list:
    name, n_files, size, mq = get_dataset_info(dataset_name)
    # # convert total size in TB
    size_TB = size / 1e12
    gLogger.notice('|%s|%d|%.2f|' % (name, n_files, size_TB))
    total_size += size_TB
    total_n_files += n_files
  gLogger.notice('| Total | %d | %.2f |\n' % (total_n_files, total_size))
    
  DIRAC.exit()

if __name__ == '__main__':
  main()
