import unittest
from mangawalk.scraping.comick import ComicK
from mangawalk.scraping.types.type_comick import *
from mangawalk.scraping.types.type_mangawalk import *
import time
from catswalk.scraping.types.type_webdriver import *
from catswalk.utils.functional import calc_time
import os
from catswalk.scraping.webdriver import CWWebDriver
from catswalk.scraping.request import CWRequest

class TestComicK(unittest.TestCase):
    binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    executable_path = "/Users/rv/ws/tools/chromedriver"
    proxy = None
    headless = True
    url_list = ["https://comic.k-manga.jp/title/95912/pv", "https://comic.k-manga.jp/title/94017/pv", "https://comic.k-manga.jp/title/109519/pv"]


    def get_cw_driver(self, binary_location: str = None, executable_path: str = None, execution_env: EXECUTION_ENV = EXECUTION_ENV.LOCAL,  device: DEVICE = DEVICE.DESKTOP_GENERAL, proxy: str = None):
        return CWWebDriver(binary_location=binary_location, executable_path=executable_path, execution_env=execution_env, proxy=proxy, device=device)

    def get_cw_request(self):
        return CWRequest()

    def get_url_list(self):
        input_url = os.getcwd() + "/input/manga_target.csv"
        with open(input_url) as f:
            url_list = f.read().split("\n")
        return url_list

    @calc_time()
    def get_review_list(self):
        """[python -m unittest tests.scraping.test_comick.TestComicK.get_review_list]
        """
        cw_request = self.get_cw_request()
        pv_result = ComicK.get_pv(cw_request=cw_request, url="https://comic.k-manga.jp/title/133626/pv")
        results = ComicK.get_review_list(cw_request=cw_request, pv_result=pv_result)
        cw_request.close()
        output_path = os.getcwd() + "/output"
        Review.write_as_csv(results, output_path, "get_review_list")
        print(results)

    @calc_time()
    def test_get_pv(self):
        """[python -m unittest tests.scraping.test_comick.TestComicK.test_get_pv]
        """
        cw_request = self.get_cw_request()
        result = ComicK.get_pv(cw_request, "https://comic.k-manga.jp/title/94017/pv")
        print(result)

    @calc_time()
    def test_get_vol(self):
        """[python -m unittest tests.scraping.test_comick.TestComicK.test_get_vol]
        """
        result = ComicK.get_vol("https://comic.k-manga.jp/title/95912/vol/2")
        print(result)
    
    @calc_time()
    def test_get_pvs(self):
        """[python -m unittest tests.scraping.test_comick.TestComicK.test_get_pvs]
        """
        #request = ComicK(binary_location=self.binary_location, executable_path=self.executable_path, execution_env=EXECUTION_ENV.LOCAL_HEADLESS, device = DEVICE.MOBILE_GALAXY_S5)
        #request.init()
        url_list = self.get_url_list()
        results = ComicK.get_pvs(self.url_list)
        print(results)

    # get_pv_summary
    @calc_time()
    def get_pv_summary_list(self):
        """[python -m unittest tests.scraping.test_comick.TestComicK.get_pv_summary_list]
        """
        url_list = self.get_url_list()
        #url_list = self.url_list
        results = ComicK.get_pv_summary_list(url_list)
        #output_path = os.getcwd() + "/output"
        #PVResultSummary.write_as_csv(results, output_path, "get_pv_summary_list")
        print(results)

    # get_pv_summary
    @calc_time()
    def get_pv_summary(self):
        """[python -m unittest tests.scraping.test_comick.TestComicK.get_pv_summary]
        """
        cw_request = self.get_cw_request()
        pv_result = ComicK.get_pv(cw_request=cw_request, url="https://comic.k-manga.jp/title/133626/pv")
        results = ComicK.get_pv_summary(cw_request, pv_result)
        print(results)

    @calc_time()
    def get_all_seriese_pv(self):
        """[python -m unittest tests.scraping.test_comick.TestComicK.get_all_seriese_pv]
        """
        result = ComicK.get_all_seriese_pv("https://comic.k-manga.jp/title/95912/pv")
        print(result)

    @calc_time()
    def test_save_comiclist_img(self):
        """[python -m unittest tests.scraping.test_comick.TestComicK.test_save_comiclist_img]
        """
        # ls, cw_web_driver: CWWebDriver,output_path: str, url: str, filename: str = "comiclist_img"
        request = CWWebDriver(binary_location=self.binary_location, executable_path=self.executable_path, execution_env=EXECUTION_ENV.LOCAL,  device = DEVICE.MOBILE_GALAXY_S5)
        results = ComicK.save_comiclist_img(request, "/Users/rv/Desktop", "https://comic.k-manga.jp/title/95912/pv")
        print(results)

    @calc_time()
    def save_top_capture(self):
        """[python -m unittest tests.scraping.test_comick.TestComicK.save_top_capture]
        """
        # ls, cw_web_driver: CWWebDriver,output_path: str, url: str, filename: str = "comiclist_img"
        request = CWWebDriver(binary_location=self.binary_location, executable_path=self.executable_path, execution_env=EXECUTION_ENV.LOCAL,  device = DEVICE.MOBILE_GALAXY_S5)
        results = ComicK.save_top_capture(request, "/Users/rv/Desktop", "https://comic.k-manga.jp/title/95912/pv")
        print(results)

    @calc_time()
    def save_thumbnail(self):
        """[python -m unittest tests.scraping.test_comick.TestComicK.save_thumbnail]
        """
        # ls, cw_web_driver: CWWebDriver,output_path: str, url: str, filename: str = "comiclist_img"
        request = self.get_cw_request()
        # , thumbnail_url: str, output_path: str, filename: str = "comiclist_img"
        results = ComicK.save_thumbnail(request, "https://cf.image-cdn.k-manga.jp/cover_320/13/133626/b133626_1_320.jpg", "/Users/rv/Desktop", "test.jpg")
        print(results)

    @calc_time()
    def output_pv_result_with_capture_and_review(self):
        """[python -m unittest tests.scraping.test_comick.TestComicK.output_pv_result_with_capture_and_review]
        """
        cw_web_driver = self.get_cw_driver(binary_location=self.binary_location, executable_path=self.executable_path, execution_env=EXECUTION_ENV.LOCAL_HEADLESS,  device = DEVICE.MOBILE_GALAXY_S5)
        #cw_web_driver.init()
        cw_request = self.get_cw_request()
        output_path = os.getcwd() + "/output"
        url = "https://comic.k-manga.jp/title/123559/pv"
        ComicK().output_pv_result_with_capture_and_review(cw_request=cw_request, cw_web_driver=cw_web_driver, url=url, output_path=output_path)

        cw_web_driver.close()
        cw_request.close()

    @calc_time()
    def write_pv_result_with_capture_and_review(self):
        """[python -m unittest tests.scraping.test_comick.TestComicK.write_pv_result_with_capture_and_review]
        """
        cw_web_driver = self.get_cw_driver(binary_location=self.binary_location, executable_path=self.executable_path, execution_env=EXECUTION_ENV.LOCAL_HEADLESS,  device = DEVICE.MOBILE_GALAXY_S5)
        #cw_web_driver.init()
        cw_request = self.get_cw_request()
        output_path = os.getcwd() + "/output"
        url = "https://comic.k-manga.jp/title/95912/pv"
        ComicK.write_pv_result_with_capture_and_review(cw_request=cw_request, cw_web_driver=cw_web_driver, url_list=self.get_url_list(), output_path=output_path)
        cw_web_driver.close()
        cw_request.close()

    @calc_time()
    def test_get_rank(self):
        """[python -m unittest tests.scraping.test_comick.TestComicK.test_get_rank]
        """
        rr = ComicK.get_rank()
        for r in rr:
            print(r)
        #time.sleep(10)


if __name__ == "__main__":
    unittest.main()