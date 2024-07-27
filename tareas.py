import sqlite3
import random

def initialize_database():
    with sqlite3.connect('tasks.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Tasks (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Description TEXT,
                IsCompleted INTEGER
            )
        ''')
        conn.commit()

class Task:
    def __init__(self, id, description, is_completed=False):
        self.id = id
        self.description = description
        self.is_completed = is_completed

class TaskManager:
    def __init__(self):
        self.connection = sqlite3.connect('tasks.db')
        self.cursor = self.connection.cursor()

    def add_task(self, task):
        self.cursor.execute('INSERT INTO Tasks (Description, IsCompleted) VALUES (?, ?)',
                            (task.description, int(task.is_completed)))
        self.connection.commit()

    def remove_task(self, task_id):
        self.cursor.execute('DELETE FROM Tasks WHERE Id = ?', (task_id,))
        self.connection.commit()

    def update_task(self, task):
        self.cursor.execute('UPDATE Tasks SET Description = ?, IsCompleted = ? WHERE Id = ?',
                            (task.description, int(task.is_completed), task.id))
        self.connection.commit()

    def get_all_tasks(self):
        self.cursor.execute('SELECT Id, Description, IsCompleted FROM Tasks')
        rows = self.cursor.fetchall()
        return [Task(id=row[0], description=row[1], is_completed=bool(row[2])) for row in rows]

    def close(self):
        self.connection.close()

def main():
    initialize_database()
    task_manager = TaskManager()

    while True:
        print("\n1. Añadir tarea")
        print("2. Actualizar tarea")
        print("3. Eliminar tarea")
        print("4. Marcar tarea como completada")
        print("5. Ver tareas")
        print("6. Salir")
        choice = input("Seleccione una opción: ")

        if choice == '1':
            description = input("Ingrese la descripción de la tarea: ")
            task = Task(id=None, description=description)  # El ID se asigna automáticamente
            task_manager.add_task(task)
            print("¡Tarea añadida!")

        elif choice == '2':
            task_id = int(input("Ingrese el ID de la tarea a actualizar: "))
            new_description = input("Ingrese una nueva descripción: ")
            tasks = task_manager.get_all_tasks()
            task_to_update = next((t for t in tasks if t.id == task_id), None)
            if task_to_update:
                task_to_update.description = new_description
                task_manager.update_task(task_to_update)
                print("¡Tarea actualizada!")
            else:
                print("¡Tarea no encontrada!")

        elif choice == '3':
            task_id = int(input("Ingrese el ID de la tarea a eliminar: "))
            task_manager.remove_task(task_id)
            print("¡Tarea eliminada!")

        elif choice == '4':
            task_id = int(input("Ingrese el ID de la tarea a marcar como completada: "))
            tasks = task_manager.get_all_tasks()
            task_to_complete = next((t for t in tasks if t.id == task_id), None)
            if task_to_complete:
                task_to_complete.is_completed = True
                task_manager.update_task(task_to_complete)
                print("¡Tarea marcada como completada!")
            else:
                print("¡Tarea no encontrada!")

        elif choice == '5':
            tasks = task_manager.get_all_tasks()
            for t in tasks:
                status = "Sí" if t.is_completed else "No"
                print(f"ID: {t.id}, Descripción: {t.description}, Completada: {status}")

        elif choice == '6':
            task_manager.close()
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida, por favor ingrese nuevamente.")

if __name__ == "__main__":
    main()
