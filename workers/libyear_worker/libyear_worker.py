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

import workers.libyear_worker.Libyear

class LibyearWorker(Worker):
    """ Worker that collects data from Repository and stores it in our database
    task: most recent task the broker added to the worker's queue
    child: current process of the queue being ran
    queue: queue of tasks to be fulfilled
    config: holds info like api keys, descriptions, and database connection strings
    """
    def __init__(self, config={}):
    #worker name
        worker_type = 'libyear_worker'

    # What is given to the worker
        given = [['github_url']]
        models = ['issues']

    # Just tables you are going to add data to.
        data_tables = ['repo_libyears']

    # These are taken care of, and are the same for every worker.
        operations_tables = ['worker_history', 'worker_job']

    # These 3 are included in every tuple the worker inserts (data collection info)
        self.tool_source = 'Libyear Worker'
        self.tool_version = '1.0.0'
        self.data_source = 'Github and Libyear'

    #get paths and call generate libyear data
    def libyear_model(self, entry_libyear_info, repo_id):
        """ Data collection and storage method
        """
        self.logger.info(entry_libyear_info)
        self.logger.info(repo_id)

        repo_path_sql = s.sql.text("""
            SELECT repo_id, CONCAT(repo_group_id || chr(47) || repo_path || repo_name) AS path
            FROM repo
            WHERE repo_id = :repo_id
        """)

        relative_repo_path = self.db.execute(repo_path_sql, {'repo_id': repo_id}).fetchone()[1]
        absolute_repo_path = self.config['repo_directory'] + relative_repo_path

        try:
            self.generate_libyear_data(repo_id, absolute_repo_path)
        except Exception as e:
            self.logger.error(e)

        self.register_task_completion(entry_info, repo_id, "libyear")

    def generate_libyear_data(self, repo_id, path):
        """Runs scc on repo and stores data in database

        :param repo_id: Repository ID
        :param path: Absolute path of the Repostiory
        """
        self.logger.info('Running `scc`....')
        self.logger.info(f'Repo ID: {repo_id}, Path: {path}')

        #calculate libyears here
        libyear = Libyear()
        calc_libyear = libyear.get_libyear(path)

        repo_libyear = {
            'repo_id': repo_id,
            'repo_libyears': calc_libyear,
            'repo_path': path,
            'tool_source': self.tool_source,
            'tool_version': self.tool_version,
            'data_source': self.data_source,
            'data_collection_date': datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        }

        result = self.db.execute(self.repo_labor_table.insert().values(repo_labor))
        self.logger.info(f"Added Repo Libyear Data: {result.inserted_primary_key}")

