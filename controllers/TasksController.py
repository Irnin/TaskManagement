from controllers.TaskController import TaskController
from models.TaskModel import TaskModel
from views.TasksView import TasksView

class TasksController:
    def __init__(self, controller):
        self.masterController = controller
        self.masterModel = controller.model
        self.masterView = controller.view

        self.model = TaskModel(self.masterModel)
        self.view = TasksView(self.masterView, self)

    def fetch_unassigned_tasks(self, page: int, page_size: int):
        return self.model.fetch_unassigned_tasks(page, page_size)

    def open_task(self, task_id):
        task_controller = TaskController(self.view, self.masterController)
        self.view.update_header(f"Task {task_id}")

        self.view.load_subpage(task_controller.view)