from dataclasses import dataclass
import csv
from mangawalk.utils.dateutils import created_at
import logging

logger = logging.getLogger()
@dataclass
class PVResult:
    """[summary]
    """
    id: str
    url: str
    title: str
    author: str
    delivered_volume: str
    is_complete: str
    magazine: str  # 掲載雑誌
    gen: str  # ジャンル
    category: str  # カテゴリ(or キーワード)
    overview: str
    has_free: bool
    thumbnail_url: str

    @classmethod
    def csv_header(cls):
        return f"id,url,title,author,delivered_volume,is_complete,magazine,gen,category,overview,has_fre,thumbnail_url"

    def to_csv_format(self):
        return f"{self.id},{self.url},{self.title},{self.author},{self.delivered_volume},{self.is_complete},{self.magazine},{self.gen},{self.category},{self.overview},{self.has_free},{self.thumbnail_url}"


@dataclass
class PVResultSummary:
    """[summary]
    """
    pv_result: str
    max_price: str
    min_price: str
    latest_pv_url: str

    @classmethod
    def from_pv_result(cls, pv_result: PVResult, max_price: str, min_price: str):
        """[summary]

        Args:
            r (PVResult): [description]
            max_price (str): [description]
            min_price (str): [description]

        Returns:
            [type]: [description]
        """
        return PVResultSummary(
            pv_result=pv_result,
            max_price=max_price,
            min_price=min_price,
            latest_pv_url=latest_pv_url
        )

    @classmethod
    def csv_header(cls):
        return f"{PVResult.csv_header()},max_price,min_price"

    def to_csv_format(self):
        return f"{self.pv_result.to_csv_format()},{self.max_price},{self.min_price}"

    @classmethod
    def write_as_csv(cls, r, path: str, filename: str) -> str:
        """[summary]

        Args:
            r ([type]): [description]
            path (str): [description]
            filename (str): [description]

        Returns:
            str: [description]
        """
        output_file = f'{path}/{filename}.csv'
        try:
            csv_str = "\n".join(list(map(lambda x: x.to_csv_format(), r)))
        except Exception as e:
            logger.error(f"PVResultSummary.write_as_csv, {r} cannot convert to csv")
        with open(output_file, 'w') as f:
            f.write(PVResultSummary.csv_header() + '\n')
            f.write(csv_str)
        return output_file


@dataclass
class VolResult:
    """[summary]
    """
    id: str
    url: str
    price: str
@dataclass
class Review:
    id: str
    comment: str
    site: str
    title: str

    @classmethod
    def csv_header(cls):
        return f"id,comment,site,title"

    def to_csv_format(self):
        return f"{self.id},{self.comment},{self.site},{self.title}"

    @classmethod
    def write_as_csv(cls, r, path: str, filename: str) -> str:
        """[summary]

        Args:
            r ([type]): [description]
            path (str): [description]
            filename (str): [description]

        Returns:
            str: [description]
        """
        output_file = f'{path}/{filename}.csv'
        csv_str = "\n".join(list(map(lambda x: x.to_csv_format(), r)))
        with open(output_file, 'w') as f:
            f.write(Review.csv_header() + '\n')
            f.write(csv_str)
        return output_file

@dataclass
class ResultLocalOutputPath:
    pv_summary_filepath: str
    review_filepath: str
    img_output_path: str

@dataclass
class PVResultSummaryWithCaptureAndReview:
    pv_result_summary: PVResultSummary
    site: str
    review_fullpath: str
    comiklist_capture_fullpath: str
    thumbnail_capture_fullpath: str
    latest_top_capture_fullpath: str
    created_at = created_at()

    @classmethod
    def csv_header(cls):
        return f"{PVResultSummary.csv_header()},site,review_fullpath,comiklist_capture_fullpath,thumbnail_capture_fullpath,latest_top_capture_fullpath,created_at"

    def to_csv_format(self):
        return f"{self.pv_result_summary.to_csv_format()},{self.site},{self.review_fullpath},{self.comiklist_capture_fullpath},{self.thumbnail_capture_fullpath},{self.latest_top_capture_fullpath},{self.created_at}"

    @classmethod
    def write_as_csv(cls, r, path: str, filename: str) -> str:
        """[summary]

        Args:
            r ([type]): [description]
            path (str): [description]
            filename (str): [description]

        Returns:
            str: [description]
        """
        output_file = f'{path}/{filename}.csv'
        # lambdaのファイル上限に引っかかるため、pandasが使えない
        # df.to_csv(output_file, sep=',', encoding='utf-8', index=False, quotechar='"', quoting=csv.QUOTE_ALL)
        csv_str = "\n".join(list(map(lambda x: x.to_csv_format(), r)))
        with open(output_file, 'w') as f:
            f.write(PVResultSummaryWithCaptureAndReview.csv_header() + '\n')
            f.write(csv_str)
        return

    def s3_upload(s3_client, local_fullpath, bucket, prefix):
        """[summary]

        Args:
            s3_client ([type]): [description]
            local_fullpath ([type]): [description]
            bucket ([type]): [description]
            prefix ([type]): [description]

        Returns:
            [type]: [description]
        """
        s3_client.upload_file(local_fullpath, bucket, prefix)
        os.remove(local_fullpath)
        return f"s3://{bucket}/{prefix}"
        
    def upload_file_to_s3(self, s3_client, bucket, prefix, local_output_path):
        """[summary]

        Args:
            s3_client ([type]): [description]
            bucket ([type]): [description]
            prefix ([type]): [description]
            local_output_path ([type]): [description]
        """
        review_s3_path = s3_upload(s3_client, self.review_fullpath, bucket, prefix + "/" + self.review_fullpath.replace(f"{local_output_path}/", ""))
        comiklist_capture_s3_path = s3_upload(s3_client, self.comiklist_capture_fullpath, bucket, prefix + "/" + self.comiklist_capture_fullpath.replace(f"{local_output_path}/", ""))
        thumbnail_capture_s3_path= s3_upload(s3_client, self.thumbnail_capture_fullpath, bucket, prefix + "/" + self.thumbnail_capture_fullpath.replace(f"{local_output_path}/", ""))
        latest_top_capture_fullpath = s3_upload(s3_client, self.latest_top_capture_fullpath, bucket, prefix + "/" +  self.latest_top_capture_fullpath.replace(f"{local_output_path}/", ""))
        return PVResultSummaryWithCaptureAndReview(
                pv_result_summary = self.pv_result_summary,
                site = self.site,
                review_fullpath = review_s3_path,
                comiklist_capture_fullpath = comiklist_capture_s3_path,
                thumbnail_capture_fullpath = thumbnail_capture_s3_path,
                latest_top_capture_fullpath = latest_top_capture_fullpath
        )

    @classmethod
    def upload_result_s3(cls, results, s3_client, bucket, prefix, local_output_path, timestamp, id):
        """[summary]

        Args:
            s3_client ([type]): [description]
            bucket ([type]): [description]
            prefix ([type]): [description]
            local_output_path ([type]): [description]
        """
        result_output_path = f"{local_output_path}/result"
        os.makedirs(result_output_path, exist_ok=True)
        result_path = PVResultSummaryWithCaptureAndReview.write_as_csv(results, result_output_path, f"pv_result_summary_{id}_{timestamp}")
        s3_path = s3_upload(result_path, bucket, prefix + "/" + result_path.replace(f"{local_output_path}/", ""))
        return s3_path