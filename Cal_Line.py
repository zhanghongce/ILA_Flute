# coding=utf-8
import os
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False
#定义代码所在的目录
base_path = '/home/gary/coding_env/DAC-2021/ILA_Flute/verification'

#在指定目录下统计所有的py文件，以列表形式返回
def collect_files(dir):
    filelist = []
    for parent,dirnames,filenames in os.walk(dir):
         for filename in filenames:
             if filename.endswith('.v'):
                 #将文件名和目录名拼成绝对路径，添加到列表里
                 filelist.append(os.path.join(parent,filename))
    return filelist

#计算单个文件内的代码行数
def calc_linenum(file):
    with open(file) as fp:
        #f = open('./verification/ADD/wrapper.v','r')
        lines = fp.readlines()
        start = lines.index( '/* GENERATE WRAPPER */\n' )
        end = lines.index( '/* END OF WRAPPER */\n' )
        number_lines = end - start - 1
        number_all_lines = len(lines)
        #print(number_lines)
    return number_lines, number_all_lines

def draw_diagram(list1,list2):
    reduced_workload = list1 #get from outside
    ISA = list2
    plt.figure(figsize=(10, 15))

    range_number = len(ISA)
    """
    绘制水平条形图方法barh
    参数一：y轴
    参数二：x轴
    """
    plt.barh(range(len(ISA)), reduced_workload , height=0.7, color='steelblue', alpha=0.8)      # 从下往上画
    #plt.barh(range(len(ISA)), reduced_workload , color='steelblue')      # 从下往上画
    plt.yticks(range(len(ISA)), ISA)
    plt.xlim(0,100)
    plt.xlabel("ratio of workload")
    plt.title("reduced workload by ILAng")
    for x, y in enumerate(reduced_workload):
        plt.text(y + 0.2, x - 0.1, '%s' % y)
    plt.show()

if __name__ == '__main__':
    files = collect_files(base_path)
    workload_ratio = []
    isa_name = []
    for f in files:
        #print(f)
        line_count, all_line_count = calc_linenum(f)
        #print('generated line count： ',number_lines)
        #print('all line count： ',all_line_count)
        #print('workload percentage: ',(line_count/all_line_count)*100,'%')
        workload_ratio.append((line_count/all_line_count)*100)
        isa_name.append(os.path.dirname(f).split('/')[-1])
        #print(isa_name)

    draw_diagram(workload_ratio,isa_name)