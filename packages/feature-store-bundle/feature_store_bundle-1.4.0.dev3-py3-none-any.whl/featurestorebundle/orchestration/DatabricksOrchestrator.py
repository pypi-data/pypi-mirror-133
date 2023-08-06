from typing import List
from pyspark.dbutils import DBUtils
from concurrent.futures import ThreadPoolExecutor
from featurestorebundle.orchestration.NotebookTask import NotebookTask


class DatabricksOrchestrator:
    def __init__(self, dbutils: DBUtils):
        self.__dbutils = dbutils

    def orchestrate(self, notebook_tasks: List[NotebookTask], num_parallel: int = 1):
        self.__submit_notebooks_parallel(notebook_tasks, num_parallel)

    def __submit_notebooks_parallel(self, notebooks: List[NotebookTask], num_parallel: int):
        with ThreadPoolExecutor(max_workers=num_parallel) as executor:
            return [executor.submit(self.__submit_notebook, notebook) for notebook in notebooks]

    def __submit_notebook(self, notebook):
        try:
            return self.__dbutils.notebook.run(notebook.path, notebook.timeout, notebook.parameters)

        except Exception:  # noqa pylint: disable=broad-except
            if notebook.retry < 1:
                raise

        notebook.retry = notebook.retry - 1

        return self.__submit_notebook(notebook)
