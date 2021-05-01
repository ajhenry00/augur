#SPDX-License-Identifier: MIT
import os, subprocess
from datetime import datetime
import logging
import requests
import json
from urllib.parse import quote
from multiprocessing import Process, Queue

import pandas as pd
import sqlalchemy as s
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import MetaData
from workers.worker_base import worker

class LibyearWorker(Worker):
    """ Worker that collects data from the Github API and stores it in our database
    task: most recent task the broker added to the worker's queue
    child: current process of the queue being ran
    queue: queue of tasks to be fulfilled
    config: holds info like api keys, descriptions, and database connection strings
    """
    def __init__(self, config={}):
        worker_type = 'libyear_worker'
## Specified in Housekeeper Block of the augur.config.json
            # {
            #     "all_focused": 1,
            #     "delay": 150000,
            #     "given": [
            #         "github_url"
            #     ],
            #     "model": "issues",
            #     "repo_group_id": 0
            # },
        given = [['github_url']]
        models = ['issues']
## Just tables you are going to add data to.
        data_tables = ['contributors', 'issues', 'issue_labels', 'message',
            'issue_message_ref', 'issue_events','issue_assignees','contributors_aliases',
            'pull_request_assignees', 'pull_request_events', 'pull_request_reviewers', 'pull_request_meta',
            'pull_request_repo']
## These are takend care of, and are the same for every worker.
        operations_tables = ['worker_history', 'worker_job']
        # These 3 are included in every tuple the worker inserts (data collection info)
        self.tool_source = 'GitHub API Worker'
        self.tool_version = '1.0.0'
        self.data_source = 'GitHub API'
        self.finishing_task = True # if we are finishing a previous task, pagination works differenty
        self.platform_id = 25150 # GitHub
        self.process_count = 1
# Most workers do not need this ...
        self.deep_collection = True
        # Run the general worker initialization
        super().__init__(worker_type, config, given, models, data_tables, operations_tables)
	
