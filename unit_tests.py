import unittest
from main import Database, Field
class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database("test_db")

    def test_create_table(self):
        # Створення таблиці
        self.db.create_table("users")
        self.assertIn("users", self.db.tables)
        
        # Спроба створити таблицю з тією ж назвою
        with self.assertRaises(ValueError):
            self.db.create_table("users")
class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database("test_db")
        self.db.create_table("users")

    def test_delete_table(self):
        # Видалення існуючої таблиці
        self.db.delete_table("users")
        self.assertNotIn("users", self.db.tables)
        
        # Спроба видалити неіснуючу таблицю
        with self.assertRaises(KeyError):
            self.db.delete_table("users")
class TestField(unittest.TestCase):
    def test_invalid_field_type(self):
        with self.assertRaises(ValueError):
            Field("age", 25, "number")  # "number" не є допустимим типом

    def test_invalid_value_type(self):
        with self.assertRaises(ValueError):
            Field("age", "25", "integer")  # Очікується int, дано str
            
class TestDatabaseIntersectTables(unittest.TestCase):
    def setUp(self):
        # Ініціалізація бази даних
        self.db = Database(name="TestDB")
        
        # Створення і заповнення таблиць
        self.db.create_table("Table1")
        self.db.create_table("Table2")
        
        # Додавання полів до першої таблиці
        self.db.tables["Table1"].add_field(Field(name="id", value=1, field_type="integer"))
        self.db.tables["Table1"].add_field(Field(name="name", value="Alice", field_type="string"))
        
        # Додавання полів до другої таблиці
        self.db.tables["Table2"].add_field(Field(name="id", value=1, field_type="integer"))
        self.db.tables["Table2"].add_field(Field(name="name", value="Bob", field_type="string"))

    def test_intersect_tables_success(self):
        # Тестування успішного перетину (збіг по полю 'id')
        result = self.db.intersect_tables("Table1", "Table2")
        self.assertIn("id", result)
        self.assertEqual(result["id"], [1])

    def test_intersect_tables_no_overlap(self):
        # Тестування відсутності збігу по імені
        result = self.db.intersect_tables("Table1", "Table2")
        self.assertNotIn("name", result)

    def test_intersect_tables_non_existent_table(self):
        # Тестування виключення, коли одна з таблиць не існує
        with self.assertRaises(KeyError):
            self.db.intersect_tables("Table1", "NonExistentTable")


if __name__ == "__main__":
    unittest.main()
