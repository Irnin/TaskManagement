from controllers.CategoryController import CategoryController
from controllers.TaskController import TaskController
from models.TaskModel import TaskModel
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

    def create_task(self):
        create_task_view = TaskCreateSubpage(self.view, self, self.is_admin)
        self.view.update_header("Create Task")

        self.view.load_subpage(create_task_view)

    def select_category(self, tk_id, tk_name):
        category_controller = CategoryController(self.masterController)
        category_controller.view.select_category(tk_id, tk_name)
