import matplotlib.pyplot as plt
import sympy as sp
import os

def Statistic(cnt, movement):
    """統計函數，負責統計運算過程中的加減乘除與函數運算"""

    for i in range(len(cnt)):
        cnt[i] += movement[i]

def ResetStatistic(cnt):
    for i in range(len(cnt)):
        cnt[i] = 0

def PrintStatistic(cnt):
    """印出統計資料"""

    name = ['加法', '減法', '乘法', '除法', '函數運算', '迭代次數']
    for i in range(6):
        print(name[i], cnt[i], sep=' : ')

def DrawGraph(progress, name='Figure 1'):
    plt.title(name)

    data = []
    for i in range(len(progress[0])):
        tmp = []
        for area in progress[1:]:
            tmp.append(area[i])
        data.append(tmp)

    colors = ['red', 'blue', 'green']
    for i in range(len(progress[0])):
        try:
            plt.plot([x for x in range(len(data[i]))], data[i], color=colors[i], marker='o')
        except:
            pass

    plt.show()

def OutputCSV(progress, name, title):
    try:
        os.mkdir('./Result')
    except:
        pass

    if not name.endswith('.csv') or not name.endswith('.txt'):
        name = './Result/' + name + ".csv"
    with open(name, 'w') as file:
        file.write(title + ',' * len(progress[0]) + '\n')
        for area in progress[1:]:
            file.write(f'{area}'[1:-1] + ',\n')

def CSVFusion(algorithms, save_file=False):
    max_len = -1
    data = []
    data_output = []

    CSVs = [x.__name__ + '.csv' for x in algorithms]

    for csv in CSVs:
        with open('./Result/' + csv, 'r') as file:
            data_str = file.readlines()
            max_len = max(max_len, len(data_str))
            data.append(data_str)
    
    for line_index in range(max_len):
        tmp_str = ''
        for csv_file in data:
            if line_index >= len(csv_file):
                for i in range(csv_file[-1].count(',')):
                    tmp_str += ','
            else:
                tmp_str += csv_file[line_index].split('\n')[0]
        tmp_str += '\n'
        data_output.append(tmp_str)

    if save_file:
        with open('./Result/Fusioned.csv', 'w') as file:
            file.writelines(data_output)
    
    return data_output
