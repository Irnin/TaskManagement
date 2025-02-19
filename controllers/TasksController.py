from controllers.AdminController import AdminController
from controllers.TaskController import TaskController
from models.TaskModel import TaskModel
from utility.logging import Logging
from views.Archive import Archive
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
        if hasattr(self, 'archive_view') and self.archive_view is not None:
            self.archive_view.destroy()

        task_controller = TaskController(self.view, self, task['idTask'], self.masterModel.is_admin())

        self.view.update_header(f"Task [{task['idTask']}] - {task['title']}")

        self.view.load_subpage(task_controller.view)

    def update_subpage(self, view):
        self.view.load_subpage(view)

    def open_task_with_id(self, task_id):
        try:
            task = self.model.get_task(task_id)
            task = task.json()
            self.open_task(task)
        except Exception as e:
            Logging.log_error(f"Can not open task with id {task_id}")
            Logging.log_error(f"Error: {e}")

    def reload_data(self):
        self.view.table.reload_data()

    def open_create_task(self):
        create_task_view = TaskCreateSubpage(self.view, self, self.is_admin)
        self.view.update_header("Create Task")

        self.view.load_subpage(create_task_view)

    def open_archive(self):
        self.view.update_header("Archive")

        self.archive_view = Archive(self.view, self)

        self.view.load_subpage(self.archive_view)

    def create_task(self, title, description, category_id, task_score, due_date):
        self.model.create_task(title, description, category_id, task_score, due_date)

    def fetch_categories(self, page: int = 0, page_size: int = 25):
        return self.model.get_categories(page=page, page_size=page_size)

    def fetch_finished_tasks(self, page: int, page_size: int):
        return self.model.fetch_finished_tasks(page, page_size)

    def delete_task(self, task_id):
        Logging.log_info(f"Deleting task with id {task_id}")
        self.model.delete_task(task_id)

        self.reload_data()

    def assign_task(self, task_id):
        user_id = self.masterModel.user.id
        task_id = int(task_id)
        self.model.assign_task(task_id, user_id)

        self.reload_data()

    def rate_task(self, task_id, rate):
        self.model.rate_task(task_id, rate)

    def finish_task(self, task_id: int):
        self.model.finish_task(task_id)