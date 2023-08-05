import requests
from lxml import etree
import json
import openpyxl
from pyecharts.charts import Pie
from pyecharts import options as opts
import pandas as pd

url = "https://voice.baidu.com/act/newpneumonia/newpneumonia"
response = requests.get(url)
# print(response.text)
# 生成HTML对象
html = etree.HTML(response.text)
result = html.xpath('//script[@type="application/json"]/text()')
result = result[0]
# json.load()方法可以将字符串转化为python数据类型
result = json.loads(result)
# 创建工作簿
wb = openpyxl.Workbook()
# 创建工作表
ws = wb.active
ws.title = "国内疫情"
ws.append(['省份', '累计确诊', '死亡', '治愈', '现有确诊', '累计确诊增量', '死亡增量', '治愈增量', '现有确诊增量'])
result_in = result['component'][0]['caseList']
data_out = result['component'][0]['globalList']
'''
area --> 大多为省份
city --> 城市
confirmed --> 累计
crued --> 值域
relativeTime -->
confirmedRelative --> 累计的增量
curedRelative --> 值域的增量
curConfirm --> 现有确镇
curConfirmRelative --> 现有确镇的增量
'''
for each in result_in:
    temp_list = [each['area'], each['confirmed'], each['died'], each['crued'], each['curConfirm'],
                 each['confirmedRelative'], each['diedRelative'], each['curedRelative'],
                 each['curConfirmRelative']]
    for i in range(len(temp_list)):
        if temp_list[i] == '':
            temp_list[i] = '0'
    ws.append(temp_list)
# 获取国外疫情数据
for each in data_out:
    sheet_title = each['area']
    # 创建一个新的工作表
    ws_out = wb.create_sheet(sheet_title)
    ws_out.append(['国家', '累计确诊', '死亡', '治愈', '现有确诊', '累计确诊增量'])
    for country in each['subList']:
        list_temp = [country['country'], country['confirmed'], country['died'], country['crued'],
                     country['curConfirm'], country['confirmedRelative']]
        for i in range(len(list_temp)):
            if list_temp[i] == '':
                list_temp[i] = '0'
        ws_out.append(list_temp)
wb.save('./data.xlsx')

df= pd.read_excel(
'./data.xlsx')



# 降序排序
df.sort_values(by='累计确诊', ascending=False, inplace=True)

color_series = ['#FAE927','#E9E416','#C9DA36','#9ECB3C','#6DBC49',
                 '#37B44E','#3DBA78','#14ADCF','#209AC9','#1E91CA',
                 '#2C6BA0','#2B55A1','#2D3D8E','#44388E','#6A368B'
                 '#7D3990','#A63F98','#C31C88','#D52178','#D5225B',
                 '#D02C2A','#D44C2D','#F57A34','#FA8F2F','#D99D21',
                 '#CF7B25','#CF7B25','#CF7B25']

# # 提取数据
v = df['省份'].values.tolist()
d = df['累计确诊'].values.tolist()

g = df['治愈'].values.tolist()

# 实例化Pie类
pie1 = Pie(init_opts=opts.InitOpts(width='1350px', height='750px'))
# 设置颜色
pie1.set_colors(color_series)
# 添加数据，设置饼图的半径，是否展示成南丁格尔图
pie1.add("", [list(z) for z in zip(v, d)],
        radius=["30%", "135%"],
        center=["50%", "65%"],
        rosetype="area"
        )
# 设置全局配置项
pie1.set_global_opts(title_opts=opts.TitleOpts(title='玫瑰图示例'),
                     legend_opts=opts.LegendOpts(is_show=False),
                     toolbox_opts=opts.ToolboxOpts())
# 设置系列配置项
pie1.set_series_opts(label_opts=opts.LabelOpts(is_show=True, position="inside", font_size=12,
                                               formatter="{b}:{c}例", font_style="italic",
                                               font_weight="bold", font_family="Microsoft YaHei"
                                               ),
                     )
pie1.render('累计确诊.html')

v = df['省份'].values.tolist()
e = df['死亡'].values.tolist()
df.sort_values(by='死亡', ascending=False, inplace=True)
pie2 = Pie(init_opts=opts.InitOpts(width='1350px', height='750px'))
# 设置颜色
pie2.set_colors(color_series)
# 添加数据，设置饼图的半径，是否展示成南丁格尔图
pie2.add("", [list(z) for z in zip(v, e)],
        radius=["30%", "135%"],
        center=["50%", "65%"],
        rosetype="area"
        )
# 设置全局配置项
pie2.set_global_opts(title_opts=opts.TitleOpts(title='玫瑰图示例'),
                     legend_opts=opts.LegendOpts(is_show=False),
                     toolbox_opts=opts.ToolboxOpts())
# 设置系列配置项
pie2.set_series_opts(label_opts=opts.LabelOpts(is_show=True, position="inside", font_size=12,
                                               formatter="{b}:{c}例", font_style="italic",
                                               font_weight="bold", font_family="Microsoft YaHei"
                                               ),
                     )
pie2.render('死亡.html')

v = df['省份'].values.tolist()
e = df['治愈'].values.tolist()
df.sort_values(by='治愈', ascending=False, inplace=True)
pie3 = Pie(init_opts=opts.InitOpts(width='1350px', height='750px'))
# 设置颜色
pie3.set_colors(color_series)
# 添加数据，设置饼图的半径，是否展示成南丁格尔图
pie3.add("", [list(z) for z in zip(v, e)],
        radius=["30%", "135%"],
        center=["50%", "65%"],
        rosetype="area"
        )
# 设置全局配置项
pie3.set_global_opts(title_opts=opts.TitleOpts(title='玫瑰图示例'),
                     legend_opts=opts.LegendOpts(is_show=False),
                     toolbox_opts=opts.ToolboxOpts())
# 设置系列配置项
pie3.set_series_opts(label_opts=opts.LabelOpts(is_show=True, position="inside", font_size=12,
                                               formatter="{b}:{c}例", font_style="italic",
                                               font_weight="bold", font_family="Microsoft YaHei"
                                               ),
                     )
pie3.render('治愈.html')

