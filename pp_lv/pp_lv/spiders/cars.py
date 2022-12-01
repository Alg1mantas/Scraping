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
        data = json.loads(response.body)
        if len(data["content"]["data"]) <= 0:
            raise CloseSpider('All pages are crawled')
        self.data_iterator(data)


    def data_iterator(self, data) -> None:
        """Iterates through given JSON data, and write the necessary data to CSV file"""      
        for _ in data["content"]["data"]:
            raw_car_info = {}
            brand = _["category"]["parent"]["parent"]["name"]
            sub_brand = _["category"]["parent"]["name"]
            model = _["category"]["name"]
            for car in _["adFilterValues"]:
                key = car["filter"]["name"]
                if car["value"] is None:
                    value = car["textValue"]
                else:
                    value = car["value"]["displayValue"]
                raw_car_info[key] = value

            car_data = []
            
            if brand != "Vieglie auto":
                    car_data.append(brand)
            car_data.append(sub_brand)
            car_data.append(model)

            if 'Izlaiduma gads' in raw_car_info:
                car_data.append(raw_car_info['Izlaiduma gads'])
            else:
                car_data.append("No data about Year")


            if 'Nobraukums, km' in raw_car_info:
                car_data.append(raw_car_info['Nobraukums, km'])
            else:
                car_data.append("No data about Mileage")


            if 'VIN kods' in raw_car_info:
                car_data.append(raw_car_info['VIN kods'])
            else:
                car_data.append("No data about VIN")


            if 'Auto numurs' in raw_car_info:
                car_data.append(raw_car_info['Auto numurs'])
            else:
                car_data.append("No data about Number Plate")
            
            if len(car_data) > 6:
                car_data.pop(1)
            
            with open(OUTPUT_FILENAME, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows([car_data])


    def csv_headers(self) -> None:
        if os.path.exists(OUTPUT_FILENAME) == False:
            with open(OUTPUT_FILENAME, 'w', newline= "") as file:
                headers = csv.DictWriter(file, delimiter=',',fieldnames=CSV_HEADERS)
                headers.writeheader()