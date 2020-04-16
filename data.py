import re
import datetime
import yaml

last_actualisation = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

recorded_sessions = 'recorded sessions.txt'
processed_sessions = 'processed sessions.txt'


def loadYaml():
    with open('config.yaml', 'r') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
        regions = data['config']['regions']
        cars = {'us': {'cars': data['cars']['us']}, 'eu': {'cars': data['cars']['eu']},
                'lam': {'cars': data['cars']['lam']}, 'apac': {'cars': data['cars']['apac']},
                'zaf': {'cars': data['cars']['zaf']}, 'rus&ukr': {'cars': data['cars']['rus&ukr']}}
        return regions, cars


def get_data_from_text_file(recorded_sessions):
    try:
        with open(recorded_sessions, 'r') as file:
            data = file.read()
        return data
    except FileNotFoundError as e:
        print(e)


recorded_data = get_data_from_text_file(recorded_sessions)
processed_data = get_data_from_text_file(processed_sessions)


def adding_to_list_of_data_without_repeats(recorded_data, processed_data):
    recorded_data += processed_data
    recorded_data = recorded_data.split('\n')
    recorded_data = set(recorded_data)
    recorded_data = list(recorded_data)
    recorded_data = '\n '.join(recorded_data)
    return recorded_data


recorded_data = adding_to_list_of_data_without_repeats(recorded_data, processed_data)


def get_number_of_months(data):
    data_list = data.split('\n')
    months = (month.split('_')[2] for month in data_list if month)
    months = sorted(months)
    return list(months)


def get_list_of_sessions(processed_sessions):
    with open(processed_sessions, 'r') as file:
        data = file.read()
        data_list = data.split('\n')
        months = get_number_of_months(get_data_from_text_file(recorded_sessions))
        full_list = [car.split('_')[0] for car in data_list if car]
        cars_list = list(set(full_list))
        car_dict = {}
        cars = []
        months_names = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        for car, session in zip(cars_list, data_list):
            if car:
                amount_of_sessions = full_list.count(car)
                car_dict['car_name'] = car
                car_dict['sessions'] = amount_of_sessions
                for month in months_names:
                    car_dict[str(month)] = 0
                cars.append(car_dict.copy())
    return cars, months_names


def find_number_of_sessions_per_month(data, cars, number_of_months):
    data_list = data.split('\n')
    for car in cars:
        car_name = car['car_name']
        for month in number_of_months:
            pattern = re.compile(rf'{car_name}_2020_{month}')
            matches = pattern.findall(data)
            car[month] = len(matches)
    return cars


def get_number_of_sessions_per_region(cars, cars_data, months):
    region = {}
    final_region = []
    for key, value in cars_data.items():
        region['region'] = key
        for car in cars:
            if car['car_name'] in value['cars']:
                for month in months:
                    region[month] = car[month]
                final_region.append(region.copy())
    regions_name = cars_data.keys()
    for region_n in regions_name:
        us = [reg for reg in final_region if reg['region'] == 'us']
        eu = [reg for reg in final_region if reg['region'] == 'eu']
        apac = [reg for reg in final_region if reg['region'] == 'apac']
        lam = [reg for reg in final_region if reg['region'] == 'lam']
        zaf = [reg for reg in final_region if reg['region'] == 'zaf']
        rus_ukr = [reg for reg in final_region if reg['region'] == 'rus&ukr']
    result = []
    temp = {}
    list = []
    for mon in months:
        sum = 0
        for u in us:
            sum += u[mon]
        list.append(sum)
    final_result = {}
    final_result['us'] = list
    list = []
    for mon in months:
        sum = 0
        for u in eu:
            sum += u[mon]
        list.append(sum)
    final_result['eu'] = list
    list = []
    for mon in months:
        sum = 0
        for u in apac:
            sum += u[mon]
        list.append(sum)
    final_result['apac'] = list
    list = []
    for mon in months:
        sum = 0
        for u in eu:
            sum += u[mon]
        list.append(sum)
    final_result['eu'] = list
    list = []
    for mon in months:
        sum = 0
        for u in lam:
            sum += u[mon]
        list.append(sum)
    final_result['lam'] = list
    list = []
    for mon in months:
        sum = 0
        for u in zaf:
            sum += u[mon]
        list.append(sum)
    final_result['zaf'] = list
    list = []
    for mon in months:
        sum = 0
        for u in rus_ukr:
            sum += u[mon]
        list.append(sum)
    final_result['rus&ukr'] = list

    return final_result


# recorded sessions
regions, cars_data = loadYaml()
cars, months = get_list_of_sessions(recorded_sessions)

final_data = find_number_of_sessions_per_month(recorded_data, cars, months)

sessions_per_region = get_number_of_sessions_per_region(cars, cars_data, months)

# processed sessions
cars, months = get_list_of_sessions(processed_sessions)
final_data_of_processed_sessions = find_number_of_sessions_per_month(processed_data, cars, months)

sessions_per_region_of_processed_data = get_number_of_sessions_per_region(cars, cars_data, months)
