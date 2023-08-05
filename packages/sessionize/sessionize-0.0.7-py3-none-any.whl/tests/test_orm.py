import unittest

from sessionize.setup_test import sqlite_setup, postgres_setup
from sessionize.session_table import SessionTable
from sessionize.utils.select import select_records
from sessionize.exceptions import ForceFail


class TestSessionTable(unittest.TestCase):
    def insert_delete_update_records(self, setup_function, schema=None):
        engine, table = setup_function(schema=schema)

        new_records = [
            {'name': 'Odos', 'age': 35},
            {'name': 'Kayla', 'age': 28}
        ]

        one_new_record = {'name': 'Jim', 'age': 27}

        updated_records = [
            {'id': 3, 'name': 'Emmy', 'age': 20},
        ]

        one_updated_record = {'id': 4, 'name': 'Noah', 'age': 21}

        with SessionTable(table.name, engine, schema=schema) as st:
            st.insert_records(new_records)
            st.insert_one_record(one_new_record)
            st.delete_records('id', [1, ])
            st.delete_one_record('id', 2)
            st.update_records(updated_records)
            st.update_one_record(one_updated_record)

        records = select_records(table, engine, schema=schema)
        expected = [
            {'id': 3, 'name': 'Emmy', 'age': 20},
            {'id': 4, 'name': 'Noah', 'age': 21},
            {'id': 5, 'name': 'Odos', 'age': 35},
            {'id': 6, 'name': 'Kayla', 'age': 28},
            {'id': 7, 'name': 'Jim', 'age': 27}
        ]
        self.assertEqual(records, expected)
    
    def test_insert_delete_update_records_sqlite(self):
        self.insert_delete_update_records(sqlite_setup)

    def test_insert_delete_update_records_postgres(self):
        self.insert_delete_update_records(postgres_setup)

    def test_insert_delete_update_records_schema(self):
        self.insert_delete_update_records(postgres_setup, schema='local')

    def insert_delete_update_records_fail(self, setup_function, schema=None):
        engine, table = setup_function(schema=schema)

        new_records = [
            {'name': 'Odos', 'age': 35},
            {'name': 'Kayla', 'age': 28}
        ]

        one_new_record = {'name': 'Jim', 'age': 27}

        updated_records = [
            {'id': 3, 'name': 'Emmy', 'age': 20},
        ]

        one_updated_record = {'id': 4, 'name': 'Noah', 'age': 21}

        try:
            with SessionTable(table.name, engine, schema=schema) as st:
                st.insert_records(new_records)
                st.insert_one_record(one_new_record)
                st.delete_records('id', [1, ])
                st.delete_one_record('id', 2)
                st.update_records(updated_records)
                st.update_one_record(one_updated_record)
                raise ForceFail
        except ForceFail:
            pass

        records = select_records(table, engine, schema=schema)
        expected = [
            {'id': 1, 'name': 'Olivia', 'age': 17},
            {'id': 2, 'name': 'Liam', 'age': 18},
            {'id': 3, 'name': 'Emma', 'age': 19},
            {'id': 4, 'name': 'Noah', 'age': 20},
        ]
        self.assertEqual(records, expected)
    
    def test_insert_delete_update_records_fail_sqlite(self):
        self.insert_delete_update_records_fail(sqlite_setup)

    def test_insert_delete_update_records_fail_postgres(self):
        self.insert_delete_update_records_fail(postgres_setup)

    def test_insert_delete_update_records_fail_schema(self):
        self.insert_delete_update_records_fail(postgres_setup, schema='local')