from scrapy.exceptions import CloseSpider
from typing import Generator
import scrapy
import json
import csv
import os


OUTPUT_FILENAME = 'pp_lv.csv'
CSV_HEADERS = (["Brand", "Model", "Year", "Mileage", "VIN", "Number Plate"])


class CarsSpider(scrapy.Spider):
    name = 'cars'

    def start_requests(self) -> Generator:
        urls = [f"""https://apipub.pp.lv/lv/api_user/v1/categories/2/lots?fV[22][type]=2363&
        orderColumn=publishDate&orderDirection=DESC&currentPage={x}&itemsPerPage=20""" for x in range (1, 500)]
        self.csv_headers()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response) -> None:
        content= json.loads(response.body)
        if len(content["content"]["data"]) <= 0:
            raise CloseSpider('All pages are crawled')
        self.data_iterator(content)


    def data_iterator(self, content) -> None:
        """Iterates through given JSON data, and write the necessary data to CSV file"""      
        for element in content["content"]["data"]:
            data = {}
            brand = element["category"]["parent"]["parent"]["name"]
            sub_brand = element["category"]["parent"]["name"]
            model = element["category"]["name"]
            for car in element["adFilterValues"]:
                key = car["filter"]["name"]
                if car["value"] is None:
                    value = car["textValue"]
                else:
                    value = car["value"]["displayValue"]
                data[key] = value

            car_info = []
            
            if brand != "Vieglie auto":
                    car_info.append(brand)
            car_info.append(sub_brand)
            car_info.append(model)

            if 'Izlaiduma gads' in data:
                car_info.append(data['Izlaiduma gads'])
            else:
                car_info.append("No data about Year")


            if 'Nobraukums, km' in data:
                car_info.append(data['Nobraukums, km'])
            else:
                car_info.append("No data about Mileage")


            if 'VIN kods' in data:
                car_info.append(data['VIN kods'])
            else:
                car_info.append("No data about VIN")


            if 'Auto numurs' in data:
                car_info.append(data['Auto numurs'])
            else:
                car_info.append("No data about Number Plate")
            
            if len(car_info) > 6:
                car_info.pop(1)
            
            with open(OUTPUT_FILENAME, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows([car_info])


    def csv_headers(self) -> None:
        if os.path.exists(OUTPUT_FILENAME) == False:
            with open(OUTPUT_FILENAME, 'w', newline= "") as file:
                headers = csv.DictWriter(file, delimiter=',',fieldnames=CSV_HEADERS)
                headers.writeheader()