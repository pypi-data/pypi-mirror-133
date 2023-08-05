import re
from typing import Union, Dict
from threading import Thread
from functools import wraps
import json

import MySQLdb as mysql
from MySQLdb.cursors import DictCursor
from MySQLdb._exceptions import OperationalError, ProgrammingError
import pandas as pd
import numpy as np

from banner.utils.const import (
    FIRST_NEWARE_DATA_TABLE, SECOND_NEWARE_DATA_TABLE, FIRST_NEWARE_AUX_TABLE, SECOND_NEWARE_AUX_TABLE, 
    NW_TEMP, CACHE_CONNECTION_KWARG, TTL_KWARG
)
from banner.utils.neware import calc_neware_cols, calc_dq_dv, merge_cache
from banner.utils.web2py import parse_w2p_to_mysql_query, COLUMN_TO_LABEL, LABEL_TO_COLUMN
from banner.connection import Connection, CacheConnection, __get_known_connection, cache_connection as cache, connections

# Handles query caching
def __cache_query(func):
    @wraps(func)
    def inner(*args, **kwargs):
        cache_connection = kwargs.get(CACHE_CONNECTION_KWARG, None) or cache()
        ttl = kwargs.get(TTL_KWARG, None)
        
        key = f'{inner.__name__}-{"_".join(str(arg) for arg in args).strip()}'

        if kwargs:
            _kwargs = "_".join([f'{key}:{str(value).strip()}' for key, value in kwargs.items()])
            key += f'-{_kwargs}'
        
        response = __cached_query(key, cache_connection)
        
        if not response.empty:
            return response
        
        response = func(*args, **kwargs)
        
        # Cache TODO USE CELERY
        Thread(
            target=__cache_query, 
            kwargs=dict(
                query=key,
                value=response,
                cache_connection=cache_connection,
                ttl=ttl
            )
        ).start()

        return response

    return inner

@__cache_query
def simple_query(query: str, connection=None, cache_connection=None, ttl=None, w2p_parse=True) -> pd.DataFrame:
    '''
        Queries a given Connection/str of a known connection (or first known) return result as DataFrame
        Cache if cache_connection or first known with ttl or default ttl for cache_connection
        Raises KeyError and OperationalError
    '''
    if not isinstance(query, str):
        return pd.DataFrame()

    connection = __get_known_connection(connection)
    
    if w2p_parse:
        query = parse_w2p_to_mysql_query(query)

    return connection.query(query)

# @__cache_query
def neware_query(device: int, unit: int, channel: int, test: int, connection: Union[Connection, str] = None, cache_connection=None, ttl=None, raw=False, dqdv=False) -> pd.DataFrame:
    '''
        Queries a given Connection(ip)/str of a known connection (or first known) return result as DataFrame
        Cache if cache_connection or first known with ttl or default ttl for cache_connection
        If dqdv -> neware.calc_dq_dv
        Raises KeyError and OperationalError
    '''
    connection = __get_known_connection(connection)
    
    # Look for the tables
    try:
        neware_data = simple_query(
            f'SELECT * FROM h_test WHERE dev_uid = {device} AND unit_id = {unit} AND chl_id = {channel} AND test_id = {test}',
            connection=connection
        ).iloc[0] # A single row is returned since we looked by primary key

    except IndexError:
        raise TypeError(f'{connection.name} has No data for device:{device}, unit:{unit}, channel:{channel}') 
    
    # Main tables into a single df
    data = pd.concat([
        simple_query(
            f'SELECT * FROM {neware_data[FIRST_NEWARE_DATA_TABLE]} WHERE unit_id = {unit} AND chl_id = {channel} AND test_id = {test}', 
            connection=connection
        ) if neware_data[FIRST_NEWARE_DATA_TABLE] else pd.DataFrame(),
        simple_query(
            f'SELECT * FROM {neware_data[SECOND_NEWARE_DATA_TABLE]} WHERE unit_id = {unit} AND chl_id = {channel} AND test_id = {test}', 
            connection=connection
        ) if neware_data[SECOND_NEWARE_DATA_TABLE] else pd.DataFrame()
    ], ignore_index=True)

    # Aux tables into a single df
    aux_data = pd.concat([
        simple_query(
            f'SELECT * FROM {neware_data[FIRST_NEWARE_AUX_TABLE]} WHERE unit_id = {unit} AND chl_id = {channel} AND test_id = {test}', 
            connection=connection
        ) if neware_data[FIRST_NEWARE_AUX_TABLE] else pd.DataFrame(),
        simple_query(
            f'SELECT * FROM {neware_data[SECOND_NEWARE_AUX_TABLE]} WHERE unit_id = {unit} AND chl_id = {channel} AND test_id = {test}', 
            connection=connection
        ) if neware_data[SECOND_NEWARE_AUX_TABLE] else pd.DataFrame()
    ], ignore_index=True)
    
    # We have temp data?
    if not aux_data.empty:
        # Unique aux columns
        aux_columns = set(np.setdiff1d(aux_data.columns, data.columns))
        # aux_data holds the correct test_tmp
        aux_columns.add(NW_TEMP)

        # data columns
        data_columns = list(data.columns)
        # aux_data holds the correct test_tmp
        data_columns.remove(NW_TEMP)

        # Add aux_columns to data
        data = pd.concat(
            [
                data[[*data_columns]],
                aux_data[[*aux_columns]]
            ], 
            axis = 1
        )
    
    if not raw:
        data = calc_neware_cols(data)
        
        if dqdv:
            data = calc_dq_dv(data)

    return data

# @__cache_query
def neware_query_by_test(table: str, cell: int, test: int, connection: Union[Connection, str] = None, cache_connection=None, ttl=None, raw=False, dqdv=False) -> pd.DataFrame:
    '''
        Queries a given Connection(ip)/str of a known connection (or first known) return result as DataFrame
        Queries the given connection for (device: int, unit: int, channel: int, test: int, connection: str) to feed neware_query
        ** Tries to merge neware_cache_query **
        Cache if cache_connection or first known with ttl or default ttl for cache_connection
        If dqdv -> neware.calc_dq_dv
        Raises OperationalError and KeyError(Failed to find a connection for given key) 
    '''
    connection = __get_known_connection(connection)
    
    # Look for the tables
    try:
        neware_keys = simple_query(
            f'SELECT device, unit, channel, test_id, ip FROM {table}_test WHERE {table}_id = {cell} AND test_id = {test}',
            connection=connection
        ).iloc[0] # A single row is returned since we looked by primary key
    
    except IndexError:
        raise TypeError(f'{connection.name} has No data for table:{table}, cell:{cell}, test:{test}') 
    
    data = neware_query(*neware_keys, raw=raw, dqdv=dqdv)

    if not raw:
        try:
            data = merge_cache(
                data,
                neware_cache_query(
                    neware_keys['ip'], neware_keys['device'], neware_keys['unit'], neware_keys['channel'], neware_keys['test_id'],
                    connection=connection
                )
            )
        
        except (TypeError, IndexError, OperationalError, ProgrammingError):
            pass
    
    return data

# @__cache_query
def neware_cache_query(ip: int, device: int, unit: int, channel: int, test: int, connection: Union[Connection, str] = None, cache_connection=None, ttl=None) -> pd.DataFrame:
    '''
        Queries a given Connection(ip)/str of a known connection (or first known) return result as DataFrame
        Cache if cache_connection or first known with ttl or default ttl for cache_connection
        Raises KeyError and OperationalError
    '''
    connection = __get_known_connection(connection)
    
    return simple_query(
        f'SELECT * FROM neware_cache WHERE ip = {ip} AND dev_uid = {device} AND unit_id = {unit} AND chl_id = {channel} AND test_id = {test}',
        connection=connection
    )

def describe_table(table, connection: Union[Connection, str] = None) -> pd.DataFrame:
    '''
        Describes a table in connection
        Raises OperationalError and KeyError(Failed to find a connection for given key) 
    '''
    connection = __get_known_connection(connection)
    
    data = simple_query(f'DESCRIBE {table}', connection)

    data['Label'] = data['Field'].map(COLUMN_TO_LABEL)

    return data

def describe(connection: Union[Connection, str] = None) -> pd.DataFrame:
    '''
        Describe Table names in connection
        Raises OperationalError and KeyError(Failed to find a connection for given key) 
    '''
    connection = __get_known_connection(connection)
    
    return simple_query(
        f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{connection.db}'",
        connection
    )

# @__cache_query
def table_query(table: str, columns: Union[list, str] = '*', condition: str = '1', connection=None, cache_connection=None, ttl=None, raw=False) -> pd.DataFrame:
    '''
        Queries a given connection for 'SELECT {columns} FROM {table} WHERE {condition}'
        Accepts both column values and labels
        raw=True - column names as in db
        Queries a given Connection(ip)/str of a known connection (or first known) return result as DataFrame
        Cache if cache_connection or first known with ttl or default ttl for cache_connection
        Raises OperationalError and KeyError(Failed to find a connection for given key) 
    '''
    if isinstance(columns, str):
        columns = list(
            map(
                str.strip,
                filter(
                    None, 
                    re.split(
                        ',|, | ,',
                        columns
                    )
                )
            )
        )
    
    _columns = [LABEL_TO_COLUMN.get(column, column) for column in columns]
    
    data = simple_query(
        f"SELECT {', '.join(_columns)} FROM {table} WHERE {condition}",
        connection=connection,
        cache_connection=cache_connection,
        ttl=ttl
    )
    
    if not raw:
        try:
            #Columns as requested!
            data.columns = columns 

        except ValueError:
            # Case columns contain *
            data.columns = [COLUMN_TO_LABEL.get(column, column) for column in data.columns]
            pass
        

    return data

def __cache_query(query, value, cache_connection: CacheConnection, ttl=None):
    try:
        assert(isinstance(cache_connection, CacheConnection))
        
        return cache_connection.cache(
            query, 
            value, 
            ttl=ttl, 
            nx=True
        )

    except Exception as e:
        print(f'Failed Caching {query} into {cache_connection}', e)
    
def __cached_query(query, cache_connection: CacheConnection):
    try:
        assert(isinstance(cache_connection, CacheConnection))
        
        cached_keys = cache_connection.query(query, keys=True)
        
        assert(cached_keys)
        
        cached = cache_connection.query(
            sorted(cached_keys), resp_type=pd.DataFrame
        )
        
        assert(isinstance(cached, pd.DataFrame))

        return cached

    except AssertionError:
        return pd.DataFrame()


    
    
    




