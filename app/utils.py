class Utils:
    @staticmethod
    def row_to_ai_prompt(data: list) -> str:
        item_name = data[1]
        base_prompt = data[2]
        keywords = data[3]
        prompt = (f'Задача: {base_prompt}. \n'
                  f' Товар: {item_name}. \n'
                  f' Ключевые слова: {keywords}')

        return prompt
