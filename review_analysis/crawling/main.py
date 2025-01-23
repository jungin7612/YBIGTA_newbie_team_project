from argparse import ArgumentParser
from typing import Dict, Type
from review_analysis.crawling.base_crawler import BaseCrawler
from review_analysis.crawling.googlemaps_crawler import GoogleMapsCrawler
from review_analysis.crawling.diningcode_crawler import DiningCodeCrawler

# 모든 크롤링 클래스를 예시 형식으로 적어주세요. 
CRAWLER_CLASSES: Dict[str, Type[BaseCrawler]] = {
    "googlemaps": GoogleMapsCrawler,
    "diningcode": DiningCodeCrawler,
}

def create_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument('-o', '--output_dir', type=str, required=True, help="Output file directory. Example: ../../database")
    parser.add_argument('-c', '--crawler', type=str, required=False, choices=CRAWLER_CLASSES.keys(),
                        help=f"Which crawler to use. Choices: {', '.join(CRAWLER_CLASSES.keys())}")
    parser.add_argument('-a', '--all', action='store_true', 
                        help="Run all crawlers. Default to False.")    
    return parser

if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    if args.all: 
        for crawler_name in CRAWLER_CLASSES.keys():
            Crawler_class = CRAWLER_CLASSES[crawler_name]
            crawler = Crawler_class(args.output_dir)
            crawler.start_browser()  # 브라우저 실행
            crawler.scrape_reviews()
            crawler.save_to_database()
            crawler.driver.quit()  # 브라우저 종료 (중요)

     
    elif args.crawler:
        Crawler_class = CRAWLER_CLASSES[args.crawler]
        crawler = Crawler_class(args.output_dir)
        crawler.start_browser()  # 브라우저 실행
        crawler.scrape_reviews()
        crawler.save_to_database()
        crawler.driver.quit()  # 브라우저 종료 (중요)

    
    else:
        raise ValueError("No crawlers.")