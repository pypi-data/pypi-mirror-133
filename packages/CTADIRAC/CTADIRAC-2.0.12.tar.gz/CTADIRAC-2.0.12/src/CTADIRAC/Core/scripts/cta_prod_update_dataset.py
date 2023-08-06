#!/usr/bin/env python

__RCSID__ = "$Id$"

import os

import DIRAC
from DIRAC.Core.Base import Script
from CTADIRAC.Core.Utilities.tool_box import read_inputs_from_file

Script.setUsageMessage("""
Update a given dataset or a list of datasets

Usage:
   %s <datasetName or ascii file with a list of datasets>
""" % Script.scriptName)

Script.parseCommandLine(ignoreErrors=True)

from DIRAC import gLogger
from DIRAC.Resources.Catalog.FileCatalogClient import FileCatalogClient

def main():
    argss = Script.getPositionalArgs()
    fc = FileCatalogClient()
    datasetList = []
    if len(argss) == 1:
      if os.path.isfile(argss[0]):
        gLogger.notice('Reading datasets from input file: %s' % argss[0])
        datasetList = read_inputs_from_file(argss[0])
      else:
        datasetList.append(argss[0])
    else:
      Script.showHelp()

    for dataset in datasetList:
      result = fc.updateDataset(dataset)

      if not result['OK']:
        gLogger.error("Failed to update dataset %s: %s" % (dataset, result['Message']))
        DIRAC.exit(-1)
      else:
        gLogger.notice("Successfully updated dataset", dataset)

    DIRAC.exit()

if __name__ == '__main__':
  main()
