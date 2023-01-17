#!/usr/bin/env python

import sys
import os
import json
import time
import logging
import logging.handlers


# Logging variables
totalLogs = len(os.listdir('logs'))
logFileName = 'logs/log_{0}.txt'.format(totalLogs)


# Set up the settings to log information as we run our build pipeline
logging.basicConfig(filename=logFileName, 
        filemode='a', 
        level=logging.INFO,
        datefmt='%H:%M:%S',
        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s')

def main(targets):
    print(targets)

if __name__ == '__main__':
    targets = [target.lower() for target in sys.argv[1:]]

    main(targets)
    logging.info('END OF BUILD.\n')