import re
import sqlite3 as sq

class logg:
    def __init__(self, h: str = None, t: str = None, r: str = None, s: str = None, ):
        self.h = h
        self.t = t
        self.r = r
        self.s = s
    def __repr__(self):
        return f'{self.h}, {self.t}, {self.r}, {self.s}'


def readConfig(filename):
    f = open(filename, 'r', encoding='UTF-8')
    lines = f.readlines()
    f.close()
    lines = [line.rstrip() for line in lines]
    directory = re.findall(r'"(.*)"', lines[0])[0].replace('\\', '/')
    return directory

def readLogs(direct):
    f = open(direct, 'r', encoding='UTF-8')
    lines = f.readlines()
    f.close()
    lines = [line.rstrip() for line in lines]
    newArr = []
    pattern = r'(^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) \[(\d{2}\/\w*\/\d{4}:\d{2}:\d{2}:\d{2} [+,-]\d{4})\] "(.*)" (\d*)'
    for line in lines:
        newLog = logg()
        newLog.h, newLog.l, newLog.u, newLog.t, newLog.r, newLog.s, newLog.b = re.split(pattern, line)[1:-1]
        newArr.append(newLog)
    return newArr

dir = readConfig('configg.txt')
logsArr = readLogs(dir)

def writeToDB(data):
    try:
        con = sq.connect('pr.db')
        cursor = con.cursor()
        print("Подключение к SQL")
        for log in data:
            cursor.execute("""INSERT OR IGNORE INTO logs
                              (h, t, r, s)
                              VALUES
                              (?, ?, ?, ?);""", [log.h, log.t, log.r, log.s])
            con.commit()
        print("Запись добавлена таблицу db.db ", cursor.rowcount)
        cursor.close()

    except sq.Error as error:
        print("Ошибка в работе SQL", error)
    finally:
        if con:
            con.close()
            print("Соединение с SQL закрыто")

writeToDB(logsArr)

###############################################################################################

def selectToUser():
    try:
        con = sq.connect('db.db')
        cursor = con.cursor()
        print("Подключение к SQL")
        print('h - ip, t - Время получения запроса, r - Первая строка запроса, s - Финальный статус')
        query = input('Введите эелементы через запятую: ')
        match input('Хотите выбрать диапазон времени? (y/n): '):
            case 'n':
                ans = cursor.execute(f"""SELECT {query} FROM logs;""").fetchall()
                con.commit()
                cursor.close()
                print(ans)
            case 'y':
                startTime = input('Введите время начала (Формат HH:MM:SS): ')
                endTime = input('Введите время конца (Формат HH:MM:SS): ')
                ans = cursor.execute(f"""select {query} FROM logs WHERE CAST((substr(t, 13, 2)||substr(t, 16, 2)||substr(t, 19, 2)) AS intege) BETWEEN {startTime.replace(':', '')} AND {endTime.replace(':', '')};""").fetchall()
                con.commit()
                cursor.close()
                print(ans)
    except sq.Error as error:
        print("Ошибка в работе SQLi", error)
    finally:
        if con:
            con.close()
            print("Соединение с SQL")

selectToUser()