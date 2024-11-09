import unittest
from . import utils
import string

dict = {
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "g",
    "д": "d",
    "е": "e",
    "ё": "yo",
    "ж": "zh",
    "з": "z",
    "и": "i",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "n",
    "о": "o",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "у": "u",
    "ф": "f",
    "х": "h",
    "ц": "c",
    "ч": "ch",
    "ш": "sh",
    "щ": "shch",
    "ь": "",
    "ы": "y",
    "ъ": "",
    "э": "r",
    "ю": "yu",
    "я": "ya",
    " ": "_",
}


class russian_in_english_test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.word = "Никита"
        cls.eng_word = "Nikita"

    #  def setUp(self):
    #      print('setUp')

    def test_russian_in_english_func(self):
        eng_func_word = utils.russian_in_english(self.word)
        
        for i in [self.word, self.eng_word, eng_func_word]:
            with self.subTest(i=i):
                self.assertIsInstance(i, str)

        self.assertTrue(set(self.word.lower()).issubset(list(dict.keys())))
        self.assertTrue(set(eng_func_word.lower()).issubset(list(dict.values())))
        self.assertTrue(set(self.eng_word.lower()).issubset(list(dict.values())))
        
        self.assertEqual(self.eng_word.lower(), eng_func_word)

        for i in range(len(self.word)):
            with self.subTest(i=i):
                self.assertEqual(self.eng_word[i].lower(), eng_func_word[i].lower())

   #  def test_check1(self):
   #      self.assertTrue("test_check1")

   #  def test_check2(self):
   #      self.assertTrue("test_check2")

#  def tearDown(self):
#      print('tearDown')

#  @classmethod
#  def tearDownClass(cls):
#      print("tearDownClass")
