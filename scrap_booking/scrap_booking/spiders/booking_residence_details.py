import pandas as pd

# Import scrapy and scrapy.crawler
import scrapy

residences = pd.read_csv("residence_urls.csv")
residence_urls = residences["url"].to_list()


class Booking_residence_detail(scrapy.Spider):
    name = "Booking_residence_detail"
    start_urls = residence_urls

    def parse(self, response):

        coordinates = response.xpath(
            "/html/body/div[@id='bodyconstraint']/div/div[@id='hotelTmpl']/div[1]/div[1]/div[1]/div[1]/div[2]/div[4]/p/a"
        ).attrib["data-atlas-latlng"]

        latitude, longitude = coordinates.split(",")

        yield {
            "name": response.xpath(
                "/html/body/div[@id='bodyconstraint']/div/div[@id='hotelTmpl']/div[@id='basiclayout']/div[1]/div[1]/div[1]/div[2]/div[4]/div[@class='hp__hotel-title pp-header']/div/div/h2/text()"
            ).get(),
            "location": response.xpath(
                "/html/body/div[@id='bodyconstraint']/div/div[@id='hotelTmpl']/div[1]/div[1]/div[1]/div[1]/div[2]/div[4]/p/span[1]/text()"
            ).get(),
            "strengths": [
                strength.xpath("div/div/div/span/div/span/text()").get()
                for strength in response.xpath(
                    "/html/body/div[@id='bodyconstraint']/div/div[@id='hotelTmpl']/div[1]/div[1]/div[2]/div/div/div[1]/div[2]/div[2]/div/div/ul/li"
                )
                if strength.xpath("div/div/div/span/div/span/text()").get() is not None
            ],
            "longitude": longitude,
            "latitude": latitude,
            "url": response.url,
        }
