import re
from collections import Counter

class TextAnalyzer:
    """
    A utility class to analyze text for word count and frequency.
    """
    def __init__(self):
        # Regex to remove punctuation but keep letters and numbers
        self.punctuation_cleaner = re.compile(r'[^\w\s]')

    def analyze(self, text):
        """
        Processes the text and returns a dictionary with word count and most frequent word.
        """
        if not text or not isinstance(text, str):
            return {"word_count": 0, "most_frequent_word": None}

        # Clean and tokenize
        clean_text = self.punctuation_cleaner.sub('', text).lower()
        words = clean_text.split()

        if not words:
            return {"word_count": 0, "most_frequent_word": None}

        counts = Counter(words)
        most_common = counts.most_common(1)[0]

        return {
            "word_count": len(words),
            "most_frequent_word": most_common[0],
            "frequency": most_common[1]
        }

def run_demo():
    analyzer = TextAnalyzer()

    # Test Case 1: 3-sentence demo paragraph requested by user
    paragraph1 = "Python is a powerful language. Python is used for automation and data science. Learning Python is fun."
    
    # Test Case 2: Technical text
    paragraph2 = "Code must be clean. Clean code is easier to maintain. Write clean code every day."
    
    # Test Case 3: Short sentence
    paragraph3 = "The quick brown fox jumps over the lazy dog."

    # Test Case 4: Repeated words with punctuation
    paragraph4 = "Apple, apple, apple! Orange; orange. Banana?"

    test_cases = [paragraph1, paragraph2, paragraph3, paragraph4]

    for i, text in enumerate(test_cases, 1):
        result = analyzer.analyze(text)
        print(f"--- Test Case {i} ---")
        print(f"Text: {text}")
        print(f"Word Count: {result['word_count']}")
        print(f"Most Frequent: '{result['most_frequent_word']}' (appeared {result.get('frequency', 0)} times)")
        print()

if __name__ == "__main__":
    run_demo()
