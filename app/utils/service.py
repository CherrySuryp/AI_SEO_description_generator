from pprint import pprint


class TextUtils:
    """
    Утилиты для работы с текстом
    """

    @staticmethod
    def row_to_ai_prompt(data: list) -> str:
        """
        Превращает несколько ячеек с данными в единый промпт для ChatGPT
        :param data:
        :return:
        """
        item_name, base_prompt, specifications, keywords = data[2:6]
        specifications = specifications.replace('\n', ', ')
        return (
            f"{base_prompt}\n"
            f"Товар: {item_name}\n"
            f"Характеристики: {specifications}\n"
            f"Ключевые слова: {keywords}"
        )

    @staticmethod
    def transform_dict_keys_to_str(data: dict):
        return ", ".join([str(i) for i in list(data.keys())])

    @staticmethod
    def count_keywords(text: str, data: list) -> str:
        """
        **Функция в разработке.**

        Проверяет вхождение ключевых слов в тексте
        :param text:
        :param data:
        :return: Возвращает ключевые слова, использованные в тексте
        """
        used_keywords = []
        keywords = data[3].split(",")
        for i in keywords:
            if i.lower() in text.lower():
                used_keywords.append(i)
        return ", ".join(used_keywords)
