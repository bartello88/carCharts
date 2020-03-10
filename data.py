import re


def get_data():
    with open('test.txt', 'r') as file:
        data = file.read()
    return data


def get_number_of_months(data):
    data_list = data.split('\n')
    months = []
    for car in data_list:
        if car:
            month = car.split('_')[2]
            months.append(month)
    months = set(months)
    months = sorted(months)
    return list(months)


def get_list_of_sessions():
    with open('test.txt', 'r') as file:
        data = file.read()
        data_list = data.split('\n')
        full_list = []
        months = get_number_of_months(get_data())
        for car in data_list:
            cars = car.split('_')[0]
            full_list.append(cars)
        cars_list = list(set(full_list))
        car_dict = {}
        lista = []
        for car, session in zip(cars_list, data_list):
            if car:

                amount_of_sessions = full_list.count(car)
                car_dict['car_name'] = car
                car_dict['sessions'] = amount_of_sessions
                for month in months:
                    car_dict[int(month)] = 0
                lista.append(car_dict.copy())
        return lista


result = get_list_of_sessions()

for i in result:
    print(i)

