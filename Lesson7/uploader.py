from Lesson7.mysql_connector import MySQLConnect


if __name__ == '__main__':
    MySQLConnect.upload_table_from_csv('data/yellow_tripdata_2018-01.csv')

