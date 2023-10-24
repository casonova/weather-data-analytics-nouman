import unittest

# import time

# importing file, functions to test
target = __import__("weather-cli")
imp = target.imp_csv_data
av = target.avg
mint = target.min_temp
maxt = target.max_temp
ht = target.hum_trend
wd = target.max_wind_day


# datasets
# ls=[1,2,3,4,5,6,7,8,9]
ls = [1, 2, 3]


class MyCustomTest(unittest.TestCase):  # tests execute in alphabetical order
    def test_a_import(self):
        self.assertEqual(imp("weather.csv"), 1, "should be 1")

    def test_b_avg_min(self):
        self.assertEqual(av(1, 100), 199.85, "should be 199.85")

    def test_c_mint(self):
        self.assertEqual(mint(1, 100), 6.1, "should be 6.1")

    def test_d_maxt(self):
        self.assertEqual(maxt(1, 100), 35.8, "should be 35.8")

    def test_e_maxt(self):
        self.assertEqual(ht(1, 100), "Decreasing", "should be Decreasing")

    def test_f_maxt(self):
        self.assertEqual(wd(1, 100), "21/02/2023", "should be 21/02/2023")


if __name__ == "__main__":
    unittest.main()
# ----------------------------------------------------------------------------------------------------------
