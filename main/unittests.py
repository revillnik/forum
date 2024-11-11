import unittest
from utils import russian_in_english
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

def str_error(z):
    if isinstance(z, str):
        raise ValueError(f"{z}")

class auto():
   def __init__(self,a,b):
      self.a = a
      self.b = b


class russian_in_english_test(unittest.TestCase):

    def compare_auto(self, a, b, msg=None):
        if a.a != b.a:
            if msg is None:
                msg = 'my error'
            self.fail(msg)

    def print():
        print('clean_up')       



    @classmethod
    def setUpClass(cls):
        cls.word = "Никита"
        cls.eng_word = "Nikita"

   #  def setUp(self):
   #      print('setUp')

    def test_russian_in_english_func(self):
        eng_func_word = russian_in_english(self.word)

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

        self.assertRaises(ValueError, str_error, "test_exc")
        self.assertRaisesRegex(ValueError, "test*", str_error, "test_exc")

        self.assertCountEqual(["a", "b"], ["a", "b"])

        self.addTypeEqualityFunc(auto, "compare_auto")

        a = auto(1,2)
        b = auto(1, 10)

        self.assertEqual(a, b, msg = 'asd')

    def test_check1(self):
         self.assertTrue("test_check1")

    def test_check2(self):
         self.assertTrue("test_check2")

class check_sute(unittest.TestCase):

    def test_check2(self):
        self.assertTrue("test_check2")


#  def tearDown(self):
#      print('tearDown')

#  @classmethod
#  def tearDownClass(cls):
#      print("tearDownClass")

test_sute = unittest.TestSuite()

test_sute.addTests([unittest.makeSuite(check_sute), unittest.makeSuite(russian_in_english_test)])

runner = unittest.TextTestRunner()

print(test_sute.countTestCases())

runner.run(test_sute)
