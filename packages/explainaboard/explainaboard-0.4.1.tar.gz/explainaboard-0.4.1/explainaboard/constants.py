from enum import Enum
import json
import enum
from typing import List, Dict
import sys, os

path_of_tasks = os.path.join(os.path.dirname(__file__), './utils/resources/tasks.json')

def get_task_mapping() -> Dict:
    with open(path_of_tasks,"r") as fin:
        task_infos = json.load(fin)
    return task_infos


def get_all_tasks() -> List[str]:
    task_infos = get_task_mapping()
    all_tasks = []
    for task_category, description in task_infos.items():
        task_list = description['options']
        all_tasks += task_list
    return all_tasks


all_tasks = get_all_tasks()
all_tasks_dict = {}
for task_name in all_tasks:
    all_tasks_dict[task_name.replace("-","_")] = task_name

TaskType = enum.Enum('TaskType', all_tasks_dict)



# class TaskType(str, Enum):
#     text_classification = "text-classification"
#     named_entity_recognition = "named-entity-recognition"
#     qa_squad = "qa-squad"
#     text_summarization = "text-summarization"


class Source(str, Enum):
    in_memory = "in_memory"  # content has been loaded in memory
    local_filesystem = "local_filesystem"
    s3 = "s3"
    mongodb = "mongodb"


class FileType(str, Enum):
    json = "json"
    tsv = "tsv"
    csv = "csv"
    conll = "conll" # for tagging task such as named entity recognition
