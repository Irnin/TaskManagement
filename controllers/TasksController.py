from controllers.CategoryController import CategoryController
from controllers.TaskController import TaskController
from models.TaskModel import TaskModel
from utility.logging import Logging
from views.TasksView import TasksView
from views.taskCreateSubpage import TaskCreateSubpage


class TasksController:
    def __init__(self, controller):
        self.masterController = controller
        self.masterModel = controller.model
        self.masterView = controller.view

        self.model = TaskModel(self.masterModel)
        self.view = TasksView(self.masterView, self)

        self.is_admin = self.masterModel.is_admin()

    def fetch_unassigned_tasks(self, page: int, page_size: int):
        return self.model.fetch_unassigned_tasks(page, page_size)

    def open_task(self, task):
        task_controller = TaskController(self.view, self, task['idTask'], self.masterModel.is_admin())

        self.view.update_header(f"Task [{task['idTask']}] - {task['title']}")

        self.view.load_subpage(task_controller.view)

    def reload_data(self):
        self.view.table.reload_data()

    def open_create_task(self):
        create_task_view = TaskCreateSubpage(self.view, self, self.is_admin)
        self.view.update_header("Create Task")

        self.view.load_subpage(create_task_view)

    def create_task(self, title, description, category_id, task_score, due_date):
        self.model.create_task(title, description, category_id, task_score, due_date)

    def select_category(self, tk_id, tk_name):
        category_controller = CategoryController(self.masterController)
        category_controller.view.select_category(tk_id, tk_name)

    def delete_task(self, task_id):
        Logging.log_info(f"Deleting task with id {task_id}")
        self.model.delete_task(task_id)

        self.reload_data()