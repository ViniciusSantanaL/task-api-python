class Task:
    tasks = []
    tasks_slug_control = 1

    def __init__(self, slug, title, description, completed=False):
        self.slug = slug
        self.title = title
        self.description = description
        self.completed = completed

    @classmethod
    def create_task_by_json(cls, title, description):
        slug = cls.tasks_slug_control
        cls.tasks_slug_control += 1
        new_task = Task(slug, title, description)
        cls.tasks.append(new_task)
        return new_task

    @classmethod
    def update_task_by_json(cls, slug, title, description, completed):
        task_to_update = cls.find_task_by_slug(slug)

        task_to_update.title = title
        task_to_update.description = description
        task_to_update.completed = completed

        return task_to_update

    @classmethod
    def delete_task_id(cls, slug):
        task_to_delete = cls.find_task_by_slug(slug)

        cls.tasks.remove(task_to_delete)
        cls.tasks_slug_control -= 1

    @classmethod
    def find_task_by_slug(cls, slug):
        for task in cls.tasks:
            if task.slug == slug:
                return task

        raise TaskNotFoundException()

    def to_dict(self):
        return {
            "slug": self.slug,
            "title": self.title,
            "description": self.description,
            "completed": self.completed
        }


class TaskNotFoundException(Exception):
    pass
