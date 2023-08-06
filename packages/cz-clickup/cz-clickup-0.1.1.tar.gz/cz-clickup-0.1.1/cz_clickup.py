from commitizen.cz.base import BaseCommitizen
from commitizen.defaults import Questions
from commitizen.cz.conventional_commits import ConventionalCommitsCz


class ClickupCz(ConventionalCommitsCz):
    def questions(self) -> Questions:
        default_questions = super().questions()
        default_questions.append({
            "type": "list",
            "name": "task",
            "message": "Select one task",
            "choices": [
                {
                    "value": "task1",
                    "name": "É a task 1",
                    "key": "oa"
                    }
                ]
            })

        return [{
            "type": "list",
            "name": "task",
            "message": "Select one task",
            "choices": [
                {
                    "value": "task1",
                    "name": "É a task 1",
                    "key": "oa"
                    }
                ]
            }]


discover_this = ClickupCz
