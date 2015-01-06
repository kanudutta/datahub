import hashlib

from account.manager import *
from core.db.connection import DataHubConnection
from core.db.manager import DataHubManager

from datahub import DataHub
from datahub.constants import *
from datahub.account.constants import *

'''
@author: anant bhardwaj
@date: Oct 9, 2013

DataHub Handler
'''

def construct_result_set(res):
  tuples = [Tuple(
      cells=[bytes(val) for val in t]) for t in res['tuples']]

  field_names = [bytes(field['name']) for field in res['fields']]
  field_types = [bytes(field['type']) for field in res['fields']]
  
  return ResultSet(status=res['status'],
                   num_tuples=res['row_count'],
                   num_more_tuples=0,
                   tuples=tuples,
                   field_names=field_names,
                   field_types=field_types)


class DataHubHandler:
  def __init__(self):
    self.sessions={}
    pass

  def get_version(self):
    return VERSION

  def open_connection(self, con_params):  
    try:
      repo_base = con_params.user

      if con_params.repo_base and con_params.repo_base != '':
        repo_base = con_params.repo_base
      
      DataHubConnection(
          user=con_params.user,
          password=hashlib.sha1(con_params.password).hexdigest(),
          repo_base=repo_base)

      con = Connection(
          user=con_params.user,
          repo_base=con_params.repo_base)

      return con
    except Exception, e:
      raise DBException(message=str(e))
  
  def create_repo(self, con, repo_name):
    try:
      manager = DataHubManager(user=con.user, repo_base=con.repo_base)
      res = manager.create_repo(repo=repo_name)
      return construct_result_set(res)
    except Exception, e:
      raise DBException(message=str(e))

  def list_repos(self, con):
    try:
      manager = DataHubManager(user=con.user, repo_base=con.repo_base)
      res = manager.list_repos()
      return construct_result_set(res)
    except Exception, e:
      raise DBException(message=str(e))

  def delete_repo(self, con, repo_name, force_if_non_empty):
    try:
      manager = DataHubManager(user=con.user, repo_base=con.repo_base)
      res = manager.delete_repo(repo=repo_name, force=force_if_non_empty)
      return construct_result_set(res)
    except Exception, e:
      raise DBException(message=str(e))

  def list_tables(self, con, repo_name):
    try:
      manager = DataHubManager(user=con.user, repo_base=con.repo_base)
      res = manager.list_tables(repo=repo_name)
      return construct_result_set(res)
    except Exception, e:
      raise DBException(message=str(e))

  def get_schema(self, con, table_name):
    try:
      manager = DataHubManager(user=con.user, repo_base=con.repo_base)
      res = manager.get_schema(table=table_name)
      return construct_result_set(res)
    except Exception, e:
      raise DBException(message=str(e))

  def execute_sql(self, con, query, query_params=None):
    try:
      manager = DataHubManager(user=con.user, repo_base=con.repo_base)
      res = manager.execute_sql(query=query, params=query_params)
      return construct_result_set(res)
    except Exception, e:
      raise DBException(message=str(e))

  def create_account(
      self, username, email, repo_name, password, app_id=None, app_token=None):
    try:
      account_register(username, email, password, repo_name, app_id, app_token)
      return True
    except Exception, e:
      raise AccountException(message=str(e))

  def remove_account(self, username, app_id=None, app_token=None):
    try:
      account_remove(username, app_id, app_token)
      return True
    except Exception, e:
      raise AccountException(message=str(e))
