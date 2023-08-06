from urllib.request import urlopen
from json import loads, dumps
from typing import List
from urllib.parse import quote_plus

from wikibase.compiler import Cmd

charset_map = dict()

# https://github.com/yuvipanda/python-wdqs/blob/master/wdqs/client.py


class WbDatabase:
    SHRT_MIN = 1
    SHRT_MAX = 1
    INT_MIN = 1
    INT_MAX = 1
    LONG_MIN = 1
    LONG_MAX = 1

    ISOLATION_LEVEL_READ_COMMITED = 1

    _MEDIAWIKI_VERSION = '_mediawiki_version'
    _INSTANCE_OF = 'instance of'
    _SUBCLASS_OF = 'subclass of'
    _DJANGO_MODEL = 'django model'
    _SPARQL_ENDPOINT = '_sparql_endpoint'

    class Error:
        ...

    class DatabaseError(BaseException):
        ...

    class IntegrityError(BaseException):
        ...

    class OperationalError(BaseException):
        ...

    class DataError(BaseException):
        ...

    class InternalError(BaseException):
        ...

    class NotSupportedError(BaseException):
        ...

    class InterfaceError(BaseException):
        ...

    class ProgrammingError(BaseException):
        ...

    @staticmethod
    def connect(charset: str = 'utf8', url: str = '',
                user: str = '', password: str = '',
                instance_of_property_id: int = None,
                subclass_of_property_id: int = None,
                django_model_item_id: int = None,
                wdqs_sparql_endpoint: str = None):
        return WbDatabaseConnection(charset, url,
                                    user, password,
                                    instance_of_property_id,
                                    subclass_of_property_id,
                                    django_model_item_id,
                                    wdqs_sparql_endpoint)


class WbCursor:

    def close(self):
        print('close')

    def execute(self, cmd, params):
        if not isinstance(cmd, dict):
            raise WbDatabase.InternalError(f'Wrong command: {cmd}')
        print(f'execute ${cmd} with ${params}')

    def fetchall(self):
        """Fetch rows from the wikibase

        Returns:
            List[Tuple]: List of rows from the wikibase
        """
        return iter(())

    def fetchone(self):
        """Fetch single row from the wikibase

        Returns:
            Tuple: the row from the wikibase
        """
        return ()


class WbApi():

    def __init__(self, url: str, charset: str = 'utf-8'):
        super().__init__()
        self.url = url
        self.charset = charset

    def mediawiki_info(self):
        return loads(urlopen(
            f'{self.url}/api.php?action=query&meta=siteinfo&format=json').read().decode(self.charset))

    def search_entities(self, query):
        if 'label' in query:
            title_search_string = query['label']
            search_result = loads(urlopen(
                f'{self.url}/api.php?action=wbsearchentities&search={quote_plus(title_search_string)}&language=en&format=json').read().decode(self.charset))
            return search_result['search']
        raise WbDatabase.InternalError('Only search by label implemented')

    def new_item(self, data):
        search_result = loads(urlopen(
            f'{self.url}/api.php?action=wbeditentity&new=item&data={quote_plus(dumps(data))}&format=json').read().decode(self.charset))
        return search_result['search']

class WbDatabaseConnection:

    def __init__(self, charset: str, url: str,
                 user: str, password: str,
                 instance_of_property_id: int,
                 subclass_of_property_id: int,
                 django_model_item_id: int,
                 wdqs_sparql_endpoint: str):
        self.charset = charset
        self.api = WbApi(url, charset)
        self.user = user
        self.password = password  # TODO: hash instead plain
        if not django_model_item_id:
            # algo: 1. select django model by name 'django model'
            #       2. if not found create the item
            #       3. if found just get the identity
            django_model_item_id = self.create_entity_if_not_found_by_name_and_get_id_without_prefix(
                'django model')

        mediawiki_info = self.api.mediawiki_info()
        wikibase_conceptbaseuri = mediawiki_info['query']['general']['wikibase-conceptbaseuri']
        # https://avangard.testo.click/api.php?action=query&meta=siteinfo&siprop=extensions&format=json
        self.wikibase_info = {
            WbDatabase._MEDIAWIKI_VERSION: mediawiki_info['query']['general']['generator'],
            WbDatabase._INSTANCE_OF: f'{wikibase_conceptbaseuri}P{instance_of_property_id}',
            WbDatabase._SUBCLASS_OF: f'{wikibase_conceptbaseuri}P{subclass_of_property_id}',
            WbDatabase._DJANGO_MODEL: f'{wikibase_conceptbaseuri}Q{django_model_item_id}',
            WbDatabase._SPARQL_ENDPOINT: wdqs_sparql_endpoint if wdqs_sparql_endpoint else f'{url}/sparql'
        }
        self.transactions = []

    def create_entity_if_not_found_by_name_and_get_id_without_prefix(self, entity_name: str) -> int:
        entities = self.api.search_entities({'label': entity_name})
        if len(entities) == 1:
            return int(entities[0]['id'][1:])
        if len(entities) == 0:
            entity = self.api.new_entity({'title': entity_name})
            return int(entity['id'][1:])
        raise WbDatabase.InternalError(
            f'The entity {entity_name} has another one (i.e. not unique)')

    def db_info(self, key):
        return self.wikibase_info.get(key)

    def cursor(self):
        return WbCursor()

    def rollback(self):
        ...

    def commit(self):
        ...

    def close(self):
        ...

    def trans(self) -> List:
        return self


class TransactionContext:

    def __init__(self, connection: WbDatabaseConnection):
        self.connection = connection

    def __enter__(self):
        # make a database connection and return it
        ...
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        # make sure the dbconnection gets closed
        self.connection.close()
        ...
