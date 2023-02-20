
class Step:
    def __init__(self, name, ) -> None:
        self.__isDone = False
        self.__contributor = "No-one"

        self.__name = name.lower()
    
    def __str__(self) -> str:
        if self.__isDone:
            return f"Шаг {self.__name}. Исполнитель: {self.__contributor}"
        return f"Шаг {self.__name} не выполнен"

    def MarkAsDone(self, contributor) -> None:
        self.__isDone = True
        self.__contributor = contributor.capitalize()
    
boba = Step("Подводка")
boba.MarkAsDone("Жека")
print(boba)
