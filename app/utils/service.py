class TextUtils:
    @staticmethod
    def row_to_ai_prompt(data: list) -> str:
        item_name, base_prompt, specifications, keywords = data[1:5]
        prompt = (
            f"{base_prompt}\n"
            f"Товар: {item_name}\n"
            f"Характеристики: {specifications}\n"
            f"Ключевые слова: {keywords}"
        )

        return prompt

    @staticmethod
    def count_keywords(text: str, data: list) -> str:
        used_keywords = []
        keywords = data[3].split(",")
        for i in keywords:
            if i.lower() in text.lower():
                used_keywords.append(i)
        return ", ".join(used_keywords)
