
import unittest
import capital_all_dirs

class MyTestCase(unittest.TestCase):

    def test_cap_all_words(self):

        # call without extra word seperatoer
        for case in [
            ['Martin hvidberg 1', 'Martin Hvidberg 1'],
            ['Martin_hvidberg 2', 'Martin_hvidberg 2']]:
            self.assertEqual(case[1], capital_all_dirs.cap_all_words(case[0]))  # Note: no extra word separator given

        # call with extra word seperatoer
        for case in [
            ['Martin hvidberg 3', 'Martin Hvidberg 3'],
            ['Martin_hvidberg 4', 'Martin_Hvidberg 4']]:
            self.assertEqual(case[1], capital_all_dirs.cap_all_words(case[0], "_"))  # Note: no extra '_' given

        # Call that is designed to be NotEqual
        for case in [
            ['Input string 0', 'Expected reply 0']]:
            self.assertNotEqual(case[1], capital_all_dirs.cap_all_words(case[0]))



if __name__ == '__main__':
    unittest.main()
