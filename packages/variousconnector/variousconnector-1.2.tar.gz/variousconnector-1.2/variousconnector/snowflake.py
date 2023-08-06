# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 22:26:47 2021

@author: weiha
"""

import snowflake.connector
import pandas as pd
from snowflake.connector.pandas_tools import pd_writer
from sqlalchemy import create_engine
import pandas
    
# In[located mudule]:

class snowflake_connector:  
    def __init__(self, credential):
        try:
            self.acccount = credential['account']
            self.user = credential['user']
            self.password = credential['pwd']
            self.warehouse = credential['warehouse']      
        except:
            credential_example = {
                'account':'XXXXX',
                'user':'user_name',
                'pwd':'password',
                'warehouse':'XXXX',
                }
            raise ValueError(f"credential format is incorrect \n"
                             f"here is an example: \n"
                             f"{credential_example}"
                             )

    
    def build_connections_by_snowflake_connector(self, db):
        connection = snowflake.connector.connect(
            account=self.acccount,
            user=self.user,
            password=self.password,
            warehouse=self.warehouse,
            database=db
            ) 
        return connection   


    def build_connection_by_SQLAlchemy(self, db, schema):
        engine = create_engine(
            'snowflake://{user}:{password}@{account}/{database}/{schema}?warehouse={warehouse}'.format(
                user=self.user,
                password=self.password,
                account=self.acccount,
                warehouse=self.warehouse,
                schema=schema,
                database=db,
                )
            )
        return engine
    
    
    def query(self, db, query):
        # build connection
        connection = self.build_connections_by_snowflake_connector(db=db)
        # run query
        query_result_df = pd.read_sql(query, connection)
        return query_result_df
    
    
    def write(self, df, db, table_name, schema,
              if_exists='fail',
              chunksize=None,
              dtype=None
              ):
        # build connection
        connection = self.build_connection_by_SQLAlchemy(db=db, schema=schema)     
        
        # write db
        df.columns = map(str.upper, df.columns)
        # due to case sensitive in snowflake, all column names convert to upper case
        # https://github.com/snowflakedb/snowflake-connector-python/issues/329#issuecomment-674549780
        
        df.to_sql(name=table_name,
                  con=connection,
                  if_exists=if_exists,
                  index=False, # snowflake doesn't support index
                  index_label=None,  # snowflake doesn't support index
                  chunksize=chunksize,
                  dtype=dtype,
                  method=pd_writer
                  )