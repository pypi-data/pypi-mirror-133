import re

# Returns a filtered dictionary by given text


class KeyWordsLocator:
    def __init__(self, file_content: str, categories: dict[str, list[str]]):
        self.file_content = file_content
        self.categories = categories

    def get_keywords(self):
        dictionary: dict[str, list[str]] = {}
        for category in self.categories:
            keywords = self.categories.get(category)
            found = filter(lambda x: re.search(x, self.file_content, re.IGNORECASE), keywords)
            dictionary[category] = list(found)

        return dictionary
