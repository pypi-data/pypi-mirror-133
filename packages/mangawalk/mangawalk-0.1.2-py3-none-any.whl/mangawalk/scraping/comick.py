from catswalk.scraping.webdriver import CWWebDriver
from catswalk.scraping.request import CWRequest
from catswalk.scraping.types.type_webdriver import EXECUTION_ENV, DEVICE, DEVICE_MODE
from mangawalk.scraping.types.type_comick import *
from mangawalk.scraping.types.type_mangawalk import *
import logging
from mangawalk.utils.dateutils import created_at
from mangawalk.utils.functional import *
import os
from catswalk.scraping.async_request import AsyncCWRequest


logger = logging.getLogger()
SITE_NAME = "comick"

class ComicKException(Exception):
    pass


class ComicK:
    def __init__(self):
        """

        Raises:
            ComicKException: [description]

        Returns:
            [type]: [description]
        """

    @classmethod
    def transition_home(cls, cw_web_driver: CWWebDriver):
        """[summary]

        Args:
            cw_web_driver (CWWebDriver): [description]
        """
        cw_web_driver.transition(url=ComicKURL.HOME.value)

    @classmethod
    def get_rank(cls, cw_request: CWRequest, comicK_rank_gen: ComicKRankGen = ComicKRankGen.TOTAL,
                 comicK_rank_duration: ComicKRankDuration = ComicKRankDuration.DAILY,
                 comicK_rank_sex: ComicKRankSex = ComicKRankSex.COMMON):
        """[summary]

        Args:
            cw_request (CWRequest): [description]
            comicK_rank_gen (ComicKRankGen, optional): [description]. Defaults to ComicKRankGen.TOTAL.
            comicK_rank_duration (ComicKRankDuration, optional): [description]. Defaults to ComicKRankDuration.DAILY.
            comicK_rank_sex (ComicKRankSex, optional): [description]. Defaults to ComicKRankSex.COMMON.

        Returns:
            [type]: [description]
        """
        base_url = ComicKURL.RANK.value

        if comicK_rank_gen != ComicKRankGen.TOTAL:
            base_url = f"{base_url}/{comicK_rank_gen.value}"

        if comicK_rank_duration != ComicKRankDuration.DAILY:
            base_url = f"{base_url}/{comicK_rank_duration.value}"

        if comicK_rank_sex != ComicKRankSex.COMMON:
            base_url = f"{base_url}/{comicK_rank_sex.value}"

        bs = cw_request.get(base_url, "html").content
        ranks = list(map(lambda x: x['href'], bs.findAll("a", {"class": "book-list--item"})))
        # pv_detail_title = list(map(lambda x: x.text, content.findAll("dt", {"class": "book-info--detail-title"})))
        return ranks

    @classmethod
    def parse_pv(cls, url, content) -> PVResult:
        id = url.split("/")[-2]
        try:
            title = content.find("h1", {"class": "book-info--title"}).find("span", {"itemprop": "name"}).text
        except Exception as e:
            m = f"{url} cannot parse, please check status. {str(e)}"
            logger.error(m)
            ComicKException(m)
        pv_detail_title = list(map(lambda x: x.text, content.findAll("dt", {"class": "book-info--detail-title"})))
        pv_detail_item = list(
            map(lambda x: x.get_text(" "), content.findAll("dd", {"class": "book-info--detail-item"})))

        if len(pv_detail_title) != len(pv_detail_item):
            raise ComicKException(
                f"pv_detail_title and pv_detail_item dosen't match {len(pv_detail_title)}, {len(pv_detail_title)}")
        pv_detail = dict(zip(pv_detail_title, pv_detail_item))

        author = pv_detail["著者・作者"]
        delivered_volume = ""
        is_complete = ""
        try:
            delivery = pv_detail["配信"].replace("\n", " ")
            delivered_volume = delivery.split("巻")[0]
            if "完結" in delivery:
                is_complete = "完結"
            else:
                is_complete = "未完結"
        except Exception:
            logger.info("parse_pv has not delivery")

        magazine = pv_detail["掲載雑誌"]
        gen = pv_detail["ジャンル"].replace("\n", " ")
        category = pv_detail["キーワード"].replace("\n", " ")
        overview = content.find("p", {"class": "book-info--desc-text"}).text.replace("\n", " ").replace(",", " ")

        # 無料判定
        book_chapter_description = content.findAll("div", {"class": "book-chapter--description"})
        has_free_list = list(map(lambda x: x.text, filter(lambda x: x, (
            map(lambda x: x.find("div", {"class": "book-chapter--bottom"}), book_chapter_description)))))
        _has_free = list(filter(lambda x: x, list(map(lambda x: ("1冊無料" in x) and ("まで1冊無料" not in x), has_free_list))))
        if len(_has_free) > 0:
            has_free = True
        else:
            has_free = False

         # book-info--left pb20
        thumbnail_url = content.find("div", {"class": "book-info--left"}).find("img").get("src")

        # レビューページ数を取得
        try:
            list_page_num = int(content.find("div", {"class": "paging__title"}).get_text(" ").split(" ")[-1])
        except Exception:
            list_page_num = 0

        pv_result = PVResult(id=id,
                             url=url,
                             title=title.replace("/", "").replace(",", " "),
                             author=author,
                             delivered_volume=delivered_volume,
                             is_complete=is_complete,
                             magazine=magazine,
                             gen=gen,
                             category=category,
                             overview=overview,
                             has_free=has_free,
                             thumbnail_url=thumbnail_url
                             )
        
        return pv_result

    @classmethod
    def parse_vol(cls, url, content) -> VolResult:
        """[summary]

        Args:
            url ([type]): [description]
            content ([type]): [description]
        """
        id = url.split("/")[-2]
        # c = content.find("div", {"id": "contents"})
        price = content.find("span", {"class": "book-chapter--pt"}).text
        result = VolResult(
            id=id,
            url=url,
            price=price
        )
        return result

    @classmethod
    def get_pv(cls, cw_request: CWRequest, url: str) -> PVResult:
        """[get pv info
        EX. https://comic.k-manga.jp/title/128536/pv]

        Args:
            cw_request (CWRequest): [description]
            url (str): [description]

        Returns:
            PVResult: [description]
        """
        logger.info(f"get_pv: {url}")

        # モバイル対応のため、contentはrequestで取得する
        content = cw_request.get(url, "html").content
        result = cls.parse_pv(url=url, content=content)
        return result

    @classmethod
    def get_pvs(cls, cw_request: CWRequest, url_list: List[str], is_async: bool = True) -> List[PVResult]:
        """[summary]

        Args:
            cw_request (CWRequest): [description]
            url_list (List[str]): [description]
            is_async (bool, optional): [description]. Defaults to True.

        Returns:
            List[PVResult]: [description]
        """
        if not is_async:
            results = list(map(lambda url: ComicK.get_pv(cw_request=cw_request, url=url), url_list))
        else:
            contents = AsyncCWRequest.execute(url_list)
            url_contents = list(zip(url_list, contents))
            results = list(map(lambda x: cls.parse_pv(x[0], x[1]), url_contents))
        return results

    @classmethod
    def get_vol(cls, cw_request: CWRequest, url: str) -> VolResult:
        logger.info(f"get_pv: {url}")

        content = cw_request.get(url, "html").content
        result = cls.parse_vol(url=url, content=content)
        return result

    @classmethod
    def get_all_series_vol(cls, cw_request: CWRequest, pv_result: PVResult, is_async: bool = True) -> List[VolResult]:
        """[summary]

        Args:
            url (str): [description]
            pv_result (PVResult): [description]
            is_async (bool, optional): [description]. Defaults to True.

        Returns:
            List[VolResult]: [description]
        """
        # vol1のURLを取得
        try:
            url_list = list(map(lambda vol: ComicKURL.VOL.value.format(pv_result.id, vol),
                                range(1, int(pv_result.delivered_volume) + 1)))
            if not is_async:
                results = list(map(lambda url: ComicK.get_pv(cw_request=cw_request, url=url), url_list))
            else:
                contents = AsyncCWRequest.execute(url_list)
                url_contents = list(zip(url_list, contents))
                results = list(map(lambda x: cls.parse_vol(x[0], x[1]), url_contents))
        except Exception:
            logger.warning(f"get_all_seriese_vol cannot get, {pv_result}")
            results = None
        return results

    @classmethod
    def get_pv_summary(cls, cw_request: CWRequest, pv_result: PVResult) -> PVResultSummary:
        """
        

        Args:
            url (str): [description]

        Returns:
            PVResultSummary: [description]
        """
        vol_results = cls.get_all_series_vol(cw_request=cw_request, pv_result=pv_result)
        if vol_results:
            prices = list(map(lambda x: x.price, vol_results))
            min_price = min(prices)
            max_price = max(prices)
            url_list = list(map(lambda x: x.url, vol_results))
            latest_pv_url = max(url_list)
        else:
            max_price = ""
            min_price = ""
            latest_pv_url = ""
        return PVResultSummary(
            pv_result=pv_result,
            max_price=max_price,
            min_price=min_price,
            latest_pv_url=latest_pv_url
        )

    @classmethod
    def get_review_list(cls, cw_request: CWRequest, pv_result: PVResult) -> List[Review]:
        """[summary]

        Args:
            cw_request (CWRequest): [description]
            pv_result (pv_result): [description]

        Returns:
            List[Review]: [description]
        """
        id = pv_result.id
        title = pv_result.title

        def pearse_review_page(content):
            return list(map(lambda x: Review(id=id, comment=x.text.replace(", ", " ").replace("\n", ""), site=SITE_NAME, title=title), content.findAll("div", {"class": "book-repo--text"})))

        first_page_url = ComicKURL.REVIEW.value.format(id, 1)
        try: 
            bs = cw_request.get(first_page_url, "html").content
            try:
                list_page_num = bs.find("div", {"class": "paging disnon"}).get_text(" ").split(" ")[-1]
                url_list = list(map(lambda vol: ComicKURL.REVIEW.value.format(id, vol), range(1, int(list_page_num) + 1)))
            except Exception:
                #print(f"cannot to get_review_list, {pv_result}")
                # レビューが1ページのみ
                url_list = [first_page_url]
            results = []
            for url in url_list:
                content = cw_request.get(url, "html").content
                r = pearse_review_page(content)
                results.append(r)
            return flatten(results)
        except Exception:
            print(f"Review not found, {first_page_url}")
            return []


    @classmethod
    def get_pv_summary_list(cls, cw_request: CWRequest, url_list: List[str]) -> List[PVResultSummary]:
        """[summary]

        Args:
            url_list (List[str]): [description]

        Returns:
            List[PVResultSummary]: [description]
        """
        pv_result_list = cls.get_pvs(url_list)
        pv_summary_list = list(map(lambda pv_result: cls.get_pv_summary(cw_request=cw_request, pv_result=pv_result), pv_result_list))
        return pv_summary_list

    @classmethod
    def save_thumbnail(cls, cw_request: CWRequest, thumbnail_url: str, output_path: str, filename: str = "comiclist_img") -> str:
        """[summary]

        Args:
            cw_request (CWRequest): [description]
            thumbnail_url (str): [description]
            output_path (str): [description]
            filename (str, optional): [filename with extention]. Defaults to "comiclist_img".

        Returns:
            str: [description]
        """
        # url: str, fullpath: str
        fullpath = f"{output_path}/{filename}"
        cw_request.download(url=thumbnail_url, fullpath=fullpath)
        return fullpath

    @classmethod
    def save_comiclist_img(cls, cw_web_driver: CWWebDriver,output_path: str, url: str, filename: str = "comiclist_img") -> str:
        """[summary]

        Args:
            output_path (str): [description]
        """
        if cw_web_driver.device.value.mode == DEVICE_MODE.MOBILE:
            logger.info("mobile")
            cw_web_driver.get(url=url)
            # wait
            cw_web_driver.wait_rendering_by_class("gaevent-detail-notlogin-bookchapter")
            cw_web_driver.wait_rendering_by_class("x-book-chapter--target")

            cw_web_driver.click_by_class_name("gaevent-detail-notlogin-bookchapter")
            logger.info("clicked")
            cw_web_driver.move_to_element_by_class_name("x-book-chapter--target")
            logger.info("moved")
            #save_path = cw_web_driver.print_screen_by_class_name(class_name="x-book-chapter--target", output_path=output_path, filename=filename)
            save_path = cw_web_driver.print_screen(path=output_path, filename=filename)
            logger.info("captured")
        else:
            logger.info("desktop")
            cw_web_driver.get(url=url)
            save_path = cw_web_driver.print_screen_by_class_name(class_name="book-chapter", output_path=output_path, filename=filename)
        return save_path

    @classmethod
    def save_top_capture(cls, cw_web_driver: CWWebDriver, url: str, output_path: str, filename: str = "top_capture") -> str:
        """[summary]

        Args:
            cw_web_driver (CWWebDriver): [description]
            url (str): [description]
            output_path (str): [description]
            filename (str, optional): [description]. Defaults to "top_capture".

        Returns:
            str: [description]
        """
        if cw_web_driver.device.value.mode == DEVICE_MODE.MOBILE:
            logger.info("mobile")
            cw_web_driver.get(url=url)
            # clearfix mt30 mb40
            cw_web_driver.wait_rendering_by_class("book-info")
            cw_web_driver.move_to_element_by_class_name("book-info")
            #save_path = cw_web_driver.print_screen_by_class_name(class_name="book-info", output_path=output_path, filename=filename)
            save_path = cw_web_driver.print_screen(path=output_path, filename=filename)
            logger.info("captured")
        else:
            logger.info("desktop")
            cw_web_driver.get(url=url)
            save_path = cw_web_driver.print_screen_by_class_name(class_name="book-chapter", output_path=output_path, filename=filename)
        return save_path

    @classmethod
    def output_pv_result_with_capture_and_review(cls, cw_request: CWRequest, cw_web_driver: CWWebDriver, url: str, output_path: str) -> PVResultSummaryWithCaptureAndReview:
        """[summary]

        Args:
            cw_request (CWRequest): [description]
            cw_web_driver (CWWebDriver): [description]
            url (url): [description]
            output_path (str): [description]

        Returns:
            PVResultWithCaptureAndReview: [description]
        """
        # mkdirs
        os.makedirs(output_path, exist_ok=True)
        comick_output_folder = f"{output_path}/comick"
        comick_output_review_folder = f"{comick_output_folder}/review"
        os.makedirs(comick_output_review_folder, exist_ok=True)

        # images
        comick_output_img_folder = f"{comick_output_folder}/img"
        os.makedirs(comick_output_img_folder, exist_ok=True)
        comiklist_capture_folder = f"{comick_output_img_folder}/comklist"
        os.makedirs(comiklist_capture_folder, exist_ok=True)
        thumbnail_capture_folder = f"{comick_output_img_folder}/thumbnail"
        os.makedirs(thumbnail_capture_folder, exist_ok=True)
        latest_top_capture_folder = f"{comick_output_img_folder}/latest_top"
        os.makedirs(latest_top_capture_folder, exist_ok=True)

        try:
            # PV
            pv_result = cls.get_pv(cw_request=cw_request, url=url)
            pv_result_summary = cls.get_pv_summary(cw_request=cw_request, pv_result=pv_result)
            content_key = f"{pv_result.title}_{created_at()}"

            # review
            revuew_list = cls.get_review_list(cw_request=cw_request, pv_result=pv_result) 
            review_fullpath = Review.write_as_csv(revuew_list, comick_output_review_folder, f"review_{content_key}")

            # image download
            comiklist_capture_fullpath = cls.save_comiclist_img(cw_web_driver=cw_web_driver, output_path=comiklist_capture_folder, url=url, filename=f"comiclist_{content_key}")
            
            # save_thumbnail(cls, cw_request: CWRequest, thumbnail_url: str, output_path: str, filename: str = "comiclist_img") 
            thumbnail_capture_fullpath = ComicK.save_thumbnail(cw_request=cw_request, thumbnail_url=pv_result_summary.pv_result.thumbnail_url, output_path=thumbnail_capture_folder, filename=f"thumbnail_{content_key}.jpg")
            # (cls, cw_web_driver: CWWebDriver,output_path: str, url: str, filename: str = "top_capture")
            if pv_result_summary.latest_pv_url != "":
                latest_top_capture_fullpath = ComicK.save_top_capture(cw_web_driver=cw_web_driver, url=pv_result_summary.latest_pv_url, output_path=latest_top_capture_folder, filename=f"top_{content_key}")
            else:
                latest_top_capture_fullpath = ""

            result = PVResultSummaryWithCaptureAndReview(
                pv_result_summary=pv_result_summary,
                site=SITE_NAME,
                review_fullpath=review_fullpath,
                comiklist_capture_fullpath=comiklist_capture_fullpath,
                thumbnail_capture_fullpath=thumbnail_capture_fullpath,
                latest_top_capture_fullpath=latest_top_capture_fullpath
            )
        except Exception as e:
            print(f"output_pv_result_with_capture_and_review,{e},{url}")
            raise ComicKException(f"{url},{str(e)}")
        return result

    @classmethod
    def write_pv_result_with_capture_and_review(cls, cw_request: CWRequest, cw_web_driver: CWWebDriver, url_list: List[str], output_path: str) -> str:
        """[summary]

        Args:
            cw_request (CWRequest): [description]
            cw_web_driver (CWWebDriver): [description]
            url (str): [description]
            output_path (str): [description]

        Returns:
            str: [description]
        """
        # mkdirs
        results = []
        for url in url_list:
            try:
                print(f"request to {url}")
                result = cls.output_pv_result_with_capture_and_review(cw_request=cw_request, cw_web_driver=cw_web_driver, url=url, output_path=output_path)
                results.append(result)
            except Exception as e:
                print(e)
        comick_output_path = f"{output_path}/comick"
        result_output_path = f"{comick_output_path}/result"
        os.makedirs(result_output_review_path, exist_ok=True)

        PVResultSummaryWithCaptureAndReview.write_as_csv(results, result_output_path, f"pv_result_summary_{created_at()}")
        #pv_result_summary_list = list(map(lambda x: x.pv_result_summary, results))
        #PVResultSummary.write_as_csv(pv_result_summary_list, result_output_review_path, f"pv_result_summary_{created_at()}")
