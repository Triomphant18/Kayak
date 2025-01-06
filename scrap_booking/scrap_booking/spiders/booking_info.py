import scrapy

cities = [
    "Mont Saint Michel",
    "St Malo",
    "Bayeux",
    "Le Havre",
    "Rouen",
    "Paris",
    "Amiens",
    "Lille",
    "Strasbourg",
    "Chateau du Haut Koenigsbourg",
    "Colmar",
    "Eguisheim",
    "Besancon",
    "Dijon",
    "Annecy",
    "Grenoble",
    "Lyon",
    "Gorges du Verdon",
    "Bormes les Mimosas",
    "Cassis",
    "Marseille",
    "Aix en Provence",
    "Avignon",
    "Uzes",
    "Nimes",
    "Aigues Mortes",
    "Saintes Maries de la mer",
    "Collioure",
    "Carcassonne",
    "Ariege",
    "Toulouse",
    "Montauban",
    "Biarritz",
    "Bayonne",
    "La Rochelle",
]


class Booking_scrape(scrapy.Spider):
    name = "Booking_info"

    # Starting URL
    start_urls = ["https://www.booking.com/index.fr.html"]

    # Parse function for login
    def parse(self, response):
        for city in cities:
            yield scrapy.FormRequest.from_response(
                response,
                formdata={"ss": city},
                callback=self.after_search,
            )

    # Callback used after login
    def after_search(self, response):

        city_name = response.url.split("ss=")[-1]

        hotels = response.xpath(
            '/html/body/div[4]/div/div[2]/div/div[2]/div[3]/div[2]/div[2]/div[3]/div[@data-testid="property-card"]'
        )
        result = {"city": city_name}
        result["info"] = []
        for hotel in hotels:

            result["info"].append(
                {
                    "name": hotel.xpath(
                        'div[1]/div[2]/div/div/div[1]/div/div[1]/div[@class="e1ee0bef81"]/h3/a/div[1]/text()',
                    ).get(),
                    "description": hotel.xpath(
                        "div[1]/div[2]/div/div/div[1]/div/div[3]/text()"
                    ).get(),
                    "url": hotel.xpath(
                        "div[1]/div[2]/div/div/div[1]/div/div[1]/div/h3/a"
                    ).attrib["href"],
                    "score": hotel.xpath(
                        "div[1]/div[2]/div/div/div[2]/div/div[1]/a/span/div/div[1]/text()"
                    ).get(),
                    "picture": hotel.xpath("div[1]/div[1]/div/a/img").attrib["src"],
                }
            )
        return result
