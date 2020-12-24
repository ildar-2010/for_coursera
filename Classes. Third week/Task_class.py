import os
import csv


class CarBase:
    file_car_type = 0
    file_brand = 1
    file_passenger_seats_count = 2
    file_photo_file_name = 3
    file_body_whl = 4
    file_carrying = 5
    file_extra = 6
    
    def __init__(self, brand, photo_file_name, carrying):
        assert brand != ''
        self.brand = brand 
        self.photo_file_name = photo_file_name
        self.get_photo_file_ext()
        self.carrying = float(carrying)

    def get_photo_file_ext(self):
        f_type = os.path.splitext(self.photo_file_name)[-1]
        assert f_type in  [".jpg", ".jpeg", ".png", ".gif"]
        return f_type
    
    @classmethod
    def instance(cls, row):
        return cls(
            row[cls.file_brand],
            row[cls.file_photo_file_name],
            row[cls.file_carrying],
            row[cls.file_passenger_seats_count],
        )


class Car(CarBase):
    car_type = 'car'

    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = int(passenger_seats_count)


class Truck(CarBase):
    car_type = 'truck'

    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        temp =  body_whl.split('x', 2)
        try:
            self.body_length = float(temp[0])
            self.body_width = float(temp[1])
            self.body_height = float(temp[2])
        except ValueError:
            self.body_length = float(0)
            self.body_width = float(0)
            self.body_height = float(0)

    def get_body_volume(self):
        return self.body_length * self.body_width * self.body_height
    
    @classmethod
    def instance(cls, row):
        return cls(
            row[cls.file_brand],
            row[cls.file_photo_file_name],
            row[cls.file_carrying],
            row[cls.file_body_whl],
        )


class SpecMachine(CarBase):
    car_type = 'spec_machine'

    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        assert extra != ''
        self.extra = extra

    @classmethod
    def instance(cls, row):
        return cls(
            row[cls.file_brand],
            row[cls.file_photo_file_name],
            row[cls.file_carrying],
            row[cls.file_extra],
        )
    

def get_car_list(csv_filename):
    car_list = []

    with open(csv_filename) as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')
        next(reader)  # пропускаем заголовок
        types = {'car': Car, 'truck': Truck, 'spec_machine': SpecMachine}
        for row in reader:
            try:
                car_type = row[CarBase.file_car_type]
            except IndexError:
                continue

            try:
                MyCar = types[car_type]
            except KeyError:
                continue
            try:
                my_car = MyCar.instance(row)
                car_list.append(my_car)
            except (IndexError, ValueError, AssertionError):
                pass

    return car_list

