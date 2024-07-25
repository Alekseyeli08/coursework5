from utils import (get_employee_data, create_database,save_data_to_database_emp)
from config import config

def main():
    # data = get_employee_data()
    # print(data)

    params = config()


    data_emp = get_employee_data()
    #data_vac = get_vacancies_data()
    create_database('hh', params)
    save_data_to_database_emp(data_emp, 'hh', params)
    #save_data_to_database_vac(data_vac, 'hh', params)

if __name__ == '__main__':
    main()




