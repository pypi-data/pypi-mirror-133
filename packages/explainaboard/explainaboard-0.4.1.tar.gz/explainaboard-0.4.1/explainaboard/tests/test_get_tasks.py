import unittest
import explainaboard
from explainaboard.constants import *

class MyTestCase(unittest.TestCase):
    def test_something(self):
        # print(get_task_mapping())
        self.assertEqual(type(get_task_mapping()), type({}))

        self.assertEqual(len(get_all_tasks()), 55)
        self.assertEqual(TaskType.text_classification.value, "text-classification")

if __name__ == '__main__':
    unittest.main()
