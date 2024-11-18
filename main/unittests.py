import unittest
from main.utils import russian_in_english
import string
from unittest.mock import patch, MagicMock, call, PropertyMock, NonCallableMock, mock_open, seal

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

class for_property_mock():
   @property
   def p(self):
      return 'p_value'
   @p.setter
   def p(self, value):
      return f'p_{value}'

def test_mock(word):
    if isinstance(word, str):
        if set(word).issubset(set(dict.keys())):
            auto_object_VW = auto.create_VW()
            auto_object_VW.create(word, word)
            if auto_object_VW.a == auto_object_VW.b == word:
                return auto_object_VW.a
            else:
                return "auto_object.a != auto_object.b"
        else:
            raise ValueError("Слово должно быть написано по-русски")
    else:
        raise TypeError("Передаваемое слово должно быть объектом класса str")


def str_error(z):
    if isinstance(z, str):
        raise ValueError(f"{z}")


class VW:

    def create(self, a, b):
        self.a = a
        self.b = b


class auto:
    dict = {}
    
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def create_VW(self, a, b):
       vw = VW()
    
    def print_wrap(self):
       print('wrap')   


class russian_in_english_test(unittest.TestCase):

    def print_clean_up(*args):
        print('clean_up')
        pass

    def compare_auto(self, a, b, msg=None):
        if a.a != b.a:
            if msg is None:
                msg = "my error"
            self.fail(msg)

    @classmethod
    def setUpClass(cls):
        cls.addClassCleanup(cls.print_clean_up)
        cls.word = "Никита"
        cls.eng_word = "Nikita"
        print("setUpClass")

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

        a = auto(1, 2)
        b = auto(1, 10)

        self.assertEqual(a, b, msg="asd")

    @patch("main.unittests.auto")
    def test_mock(self,auto_mock):

        VW_mock = MagicMock(spec=VW)
        VW_mock.create.side_effect = lambda x,y: (x, y)
        VW_mock(1)
        VW_mock(42)
        VW_mock(a=123)
        VW_mock.a = "слово"
        #   VW_mock.create.return_value = 'asd'
        #   VW_mock.create(1,2)
        #   VW_mock.create.assert_called()
        #   VW_mock.create.assert_called_with(1,2)
        VW_mock.b = "слово"
        auto_mock.create_VW.return_value = VW_mock
        self.assertEqual(test_mock('слово'), "слово")

    def test_property_mock(self):
        s = {"method.return_value": 'asd1'}
        mock = MagicMock(**s)
        with patch('main.unittests.str_error', spec=str_error, name='asd') as str_error_mock:
            mock.attach_mock(str_error_mock, "child1")
            mock.child1()
            mock.reset_mock()
        str_error_mock = MagicMock(spec=str_error, name='asd')
        mock.attach_mock(str_error_mock, 'child1')
        mock.child1()
        with patch('main.unittests.for_property_mock.p', new_callable=PropertyMock) as pr_mock:
            pr_mock.return_value='prop_mock_get'
            pr_mock = '123'
            s = for_property_mock()
            s.a = 15
            s.p = 123

        self.assertTrue("test_check2")


class check_sute(unittest.TestCase):

    @patch.multiple("main.unittests.auto", dict=PropertyMock(return_value={'a':'a'}), create_VW=MagicMock(return_value='object'))
    def test_check2(self):
        #   with patch.dict("main.unittests.auto.dict", {"a": 'asd', "b": 'asd'}) as pd:
        z = auto(1,2)
        self.assertTrue("test_check2")

    @patch("__main__.open", new_callable=mock_open, read_data='lalala')
    def test_open_mock(self, m):
        #   with patch("__main__.open", mock_open(read_data="lalalalal")) as m:
        #       with m("file", "r") as file:
        #           text_mock = file.read()
        with m("file", "r") as file:
            text_mock = file.read()
        print(text_mock)
        print(open, m)


#  def tearDown(self):
#      print('tearDown')

#  @classmethod
#  def tearDownClass(cls):
#      print("tearDownClass")

# test_sute = unittest.TestSuite()

# test_sute.addTests([unittest.makeSuite(check_sute), unittest.makeSuite(russian_in_english_test)])

# runner = unittest.TextTestRunner()

# print(test_sute.countTestCases())

# runner.run(test_sute)

if __name__ == "__main__":
    print(__name__)
    print("main")
    unittest.main()
else:
    print(__name__)
    print("import test")
