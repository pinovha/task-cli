from main import TaskManager
import pytest
from typing import Generator

@pytest.fixture
def temp_file(tmpdir) -> Generator[str, None, None]:
    tmp_file_path = tmpdir.join('tests.json')
    yield str(tmp_file_path)

def test_add_task(temp_file: str) -> None:
    manager = TaskManager(data_file=temp_file)
    manager.add_task('Test Task')
    manager.add_task('Second Task')

    assert len(manager.tasks) == 2
    assert manager.tasks[0]['description'] == 'Test Task'
    assert manager.tasks[0]['status'] == 'todo'
    assert manager.tasks[0]['id'] == 1
    assert manager.tasks[1]['id'] == 2
    assert manager.tasks[0]['createdAt'] is not None
    assert manager.tasks[0]['updatedAt'] is None

def test_del_task(temp_file: str) -> None:
    manager = TaskManager(data_file=temp_file)
    manager.add_task('Delete me')
    task_id = manager.tasks[0]['id']

    manager.del_task(task_id)
    
    assert len(manager.tasks) == 0

def test_update_task(temp_file: str) -> None:
    manager = TaskManager(data_file=temp_file)
    manager.add_task('Update Me')
    task_id = manager.tasks[0]['id']

    manager.update_task(task_id, "New Name")

    assert manager.tasks[0]['description'] == 'New Name'

def test_mark_task(temp_file: str) -> None:
    manager = TaskManager(data_file=temp_file)
    manager.add_task('Mark Me')

    manager.mark_task(1, 'done')

    assert manager.tasks[0]['status'] == 'done'