import pickle
from tkinter import Tk, Frame, Button, Label, Entry, Listbox, END, messagebox, Text, Scrollbar, filedialog, MULTIPLE

class Field:
    VALID_TYPES = {'integer', 'real', 'char', 'string', 'file', 'integerInvl'}

    def __init__(self, name, value, field_type):
        if field_type not in self.VALID_TYPES:
            raise ValueError(f"Недопустимий тип поля: {field_type}")
        self.name = name
        self.value = self.validate_value(value, field_type)
        self.type = field_type

    def validate_value(self, value, field_type):
        if field_type == 'integer':
            if not isinstance(value, int):
                raise ValueError("Значення має бути цілим числом")
        elif field_type == 'real':
            if not isinstance(value, float):
                raise ValueError("Значення має бути числом з плаваючою комою")
        elif field_type == 'char':
            if not (isinstance(value, str) and len(value) == 1):
                raise ValueError("Значення має бути одним символом")
        elif field_type == 'string':
            if not isinstance(value, str):
                raise ValueError("Значення має бути рядком")
        elif field_type == 'file':
            if not isinstance(value, str):
                raise ValueError("Значення має бути шляхом до файлу")
        elif field_type == 'integerInvl':
            if not (isinstance(value, tuple) and len(value) == 2 and all(isinstance(x, int) for x in value)):
                raise ValueError("Значення має бути кортежем з двох цілих чисел")
        return value

    def update_value(self, new_value):
        self.value = self.validate_value(new_value, self.type)

class Table:
    def __init__(self, name):
        self.name = name
        self.fields = {}

    def add_field(self, field):
        if field.name in self.fields:
            raise ValueError("Поле з таким ім'ям вже існує")
        self.fields[field.name] = field

    def update_field(self, field_name, new_value):
        if field_name not in self.fields:
            raise KeyError(f"Поле {field_name} не знайдено")
        self.fields[field_name].update_value(new_value)

    def delete_field(self, field_name):
        if field_name not in self.fields:
            raise KeyError(f"Поле {field_name} не знайдено")
        del self.fields[field_name]

class Database:
    def __init__(self, name):
        self.name = name
        self.tables = {}

    def create_table(self, table_name):
        if table_name in self.tables:
            raise ValueError("Таблиця з таким ім'ям вже існує")
        self.tables[table_name] = Table(table_name)

    def delete_table(self, table_name):
        if table_name not in self.tables:
            raise KeyError(f"Таблиця {table_name} не знайдена")
        del self.tables[table_name]

    def save_at_disk_db(self, file_path):
        with open(file_path, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load_from_disk_db(file_path):
        with open(file_path, 'rb') as f:
            return pickle.load(f)

    def show_table(self, table_name):
        if table_name not in self.tables:
            raise KeyError(f"Таблиця {table_name} не знайдена")
        table = self.tables[table_name]
        return {field_name: field.value for field_name, field in table.fields.items()}

    def intersect_tables(self, table_name1, table_name2):
        if table_name1 not in self.tables or table_name2 not in self.tables:
            raise KeyError("Одна з таблиць не існує")
        table1 = self.tables[table_name1]
        table2 = self.tables[table_name2]
        common_values = {}
        for field_name1, field1 in table1.fields.items():
            if field_name1 in table2.fields:
                field2 = table2.fields[field_name1]
                values_table1 = {field1.value}
                values_table2 = {field2.value}
                intersection = values_table1.intersection(values_table2)
                if intersection:
                    common_values[field_name1] = list(intersection)
        return common_values

class DatabaseGUI:
    def __init__(self):
        self.db = None
        self.root = Tk()
        self.root.title("Система управління базами даних")
        self.frame = Frame(self.root)
        self.frame.pack()
        Label(self.frame, text="Ім'я бази даних").grid(row=0, column=0)
        self.db_name_entry = Entry(self.frame)
        self.db_name_entry.grid(row=0, column=1)
        Button(self.frame, text="Створити БД", command=self.create_db).grid(row=0, column=2)
        Button(self.frame, text="Зберегти БД", command=self.save_db).grid(row=0, column=3)
        Button(self.frame, text="Завантажити БД", command=self.load_db).grid(row=0, column=4)
        Label(self.frame, text="Ім'я таблиці").grid(row=1, column=0)
        self.table_name_entry = Entry(self.frame)
        self.table_name_entry.grid(row=1, column=1)
        Button(self.frame, text="Створити таблицю", command=self.create_table).grid(row=1, column=2)
        Button(self.frame, text="Видалити таблицю", command=self.delete_table).grid(row=1, column=3)
        self.tables_list = Listbox(self.frame, selectmode='extended', width=50, height=15)
        self.tables_list.grid(row=2, column=0, columnspan=4)
        Label(self.frame, text="Ім'я поля").grid(row=3, column=0)
        self.field_name_entry = Entry(self.frame)
        self.field_name_entry.grid(row=3, column=1)
        Label(self.frame, text="Тип поля").grid(row=4, column=0)
        self.field_type_entry = Entry(self.frame)
        self.field_type_entry.grid(row=4, column=1)
        Label(self.frame, text="Значення поля").grid(row=5, column=0)
        self.field_value_entry = Entry(self.frame)
        self.field_value_entry.grid(row=5, column=1)
        Button(self.frame, text="Додати поле", command=self.add_field).grid(row=3, column=2)
        Button(self.frame, text="Оновити поле", command=self.update_field).grid(row=4, column=2)
        Button(self.frame, text="Видалити поле", command=self.delete_field).grid(row=5, column=2)
        Button(self.frame, text="Переглянути таблицю", command=self.view_table).grid(row=6, column=0, columnspan=4)
        Button(self.frame, text="Перетнути таблиці", command=self.intersect_tables_gui).grid(row=7, column=0, columnspan=4)
        self.table_view = Text(self.root, width=80, height=20)
        scrollbar = Scrollbar(self.root, command=self.table_view.yview)
        self.table_view.config(yscrollcommand=scrollbar.set)
        self.table_view.pack(side="left")
        scrollbar.pack(side="right", fill="y")

    def intersect_tables_gui(self):
        selected_indices = self.tables_list.curselection()
        if len(selected_indices) != 2:
            messagebox.showerror("Помилка", "Будь ласка, виберіть дві таблиці для перетину")
            return
        table1 = self.tables_list.get(selected_indices[0])
        table2 = self.tables_list.get(selected_indices[1])
        results = self.db.intersect_tables(table1, table2)
        self.table_view.delete(1.0, END)
        for name, values in results.items():
            self.table_view.insert(END, f"{name}: {values}\n")
        messagebox.showinfo("Результат перетину", f"Знайдено {len(results)} співпадінь")

    def create_db(self):
        db_name = self.db_name_entry.get()
        if not db_name:
            messagebox.showerror("Помилка", "Ім'я бази даних не може бути порожнім")
            return
        self.db = Database(db_name)
        self.tables_list.delete(0, END)
        messagebox.showinfo("Успіх", f"База даних '{db_name}' створена")

    def save_db(self):
        if not self.db:
            messagebox.showerror("Помилка", "Спочатку створіть базу даних")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".db", filetypes=[("Database files", "*.db")])
        if file_path:
            self.db.save_at_disk_db(file_path)
            messagebox.showinfo("Успіх", "База даних збережена")

    def load_db(self):
        file_path = filedialog.askopenfilename(filetypes=[("Database files", "*.db")])
        if file_path:
            self.db = Database.load_from_disk_db(file_path)
            self.tables_list.delete(0, END)
            for table_name in self.db.tables.keys():
                self.tables_list.insert(END, table_name)
            messagebox.showinfo("Успіх", "База даних завантажена")

    def create_table(self):
        if not self.db:
            messagebox.showerror("Помилка", "Спочатку створіть базу даних")
            return
        table_name = self.table_name_entry.get()
        if not table_name:
            messagebox.showerror("Помилка", "Ім'я таблиці не може бути порожнім")
            return
        try:
            self.db.create_table(table_name)
            self.tables_list.insert(END, table_name)
            messagebox.showinfo("Успіх", f"Таблиця '{table_name}' створена")
        except ValueError as e:
            messagebox.showerror("Помилка", str(e))

    def delete_table(self):
        if not self.db:
            messagebox.showerror("Помилка", "Спочатку створіть базу даних")
            return
        selected_table = self.tables_list.get(self.tables_list.curselection())
        try:
            self.db.delete_table(selected_table)
            self.tables_list.delete(self.tables_list.curselection())
            messagebox.showinfo("Успіх", f"Таблиця '{selected_table}' видалена")
        except Exception as e:
            messagebox.showerror("Помилка", str(e))

    def add_field(self):
        if not self.db:
            messagebox.showerror("Помилка", "Спочатку створіть базу даних")
            return
        selected_table = self.tables_list.get(self.tables_list.curselection())
        field_name = self.field_name_entry.get()
        field_type = self.field_type_entry.get()
        field_value = self.field_value_entry.get()

        try:
            if field_type == "integer":
                field_value = int(field_value)
            elif field_type == "real":
                field_value = float(field_value)
            elif field_type == "integerInvl":
                field_value = tuple(map(int, field_value.strip("()").split(",")))

            field = Field(field_name, field_value, field_type)
            self.db.tables[selected_table].add_field(field)
            messagebox.showinfo("Успіх", f"Поле '{field_name}' додано в таблицю '{selected_table}'")
        except Exception as e:
            messagebox.showerror("Помилка", str(e))

    def update_field(self):
        if not self.db:
            messagebox.showerror("Помилка", "Спочатку створіть базу даних")
            return
        selected_table = self.tables_list.get(self.tables_list.curselection())
        field_name = self.field_name_entry.get()
        field_value = self.field_value_entry.get()

        try:
            table = self.db.tables[selected_table]
            if table.fields[field_name].type == "integer":
                field_value = int(field_value)
            elif table.fields[field_name].type == "real":
                field_value = float(field_value)
            elif table.fields[field_name].type == "integerInvl":
                field_value = tuple(map(int, field_value.strip("()").split(",")))

            table.update_field(field_name, field_value)
            messagebox.showinfo("Успіх", f"Поле '{field_name}' оновлено")
        except Exception as e:
            messagebox.showerror("Помилка", str(e))

    def delete_field(self):
        if not self.db:
            messagebox.showerror("Помилка", "Спочатку створіть базу даних")
            return
        selected_table = self.tables_list.get(self.tables_list.curselection())
        field_name = self.field_name_entry.get()

        try:
            self.db.tables[selected_table].delete_field(field_name)
            messagebox.showinfo("Успіх", f"Поле '{field_name}' видалено")
        except Exception as e:
            messagebox.showerror("Помилка", str(e))

    def view_table(self):
        if not self.db:
            messagebox.showerror("Помилка", "Спочатку створіть базу даних")
            return
        selected_table = self.tables_list.get(self.tables_list.curselection())
        try:
            data = self.db.show_table(selected_table)
            self.table_view.delete(1.0, END)
            for field, value in data.items():
                self.table_view.insert(END, f"{field}: {value}\n")
        except Exception as e:
            messagebox.showerror("Помилка", str(e))

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    gui = DatabaseGUI()
    gui.run()
