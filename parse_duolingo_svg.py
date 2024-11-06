# parse duoling svg file
# 本文件在 copilot 生成的代码基础上修改而来，全程没有搜索引擎的帮助，只是通过阅读代码，自己理解，然后修改而来
import xml.etree.ElementTree as ET
import sys
import time

append_list = [
    # add your data here
    ["2024-11-05", 20 ],
]

def get_color(xp):
    # xp mappping color table
    # 0-74   : Aero blue      #c9ffe5
    # 75-149 : Electric blue  #7df9ff
    # 150-224: Vista blue     #7c9ed9
    # 225-299: Bleu de France #318ce7
    # 300-374: Golden yellow  #ffdf00
    # 375-449: Chrome yellow  #ffa700
    # 450-524: Cadmium orange #ed872d
    # 525-599: Carmine pink   #eb4c42
    # 600-674: Cinnabar       #e34234
    # >=675  : Red            #ff0000
    color_table = [
        "#c9ffe5","#7df9ff","#7c9ed9","#318ce7","#ffdf00",
        "#ffa700","#ed872d","#eb4c42","#e34234","#ff0000",
    ]
    return color_table[min(xp//75, 9)]

def parse_svg(svg_file):
    xml = ET.parse(svg_file)
    root = xml.getroot()
    print("Today is ", time.strftime("%Y-%m-%d", time.localtime()))

    # 2022 year data output
    sum_xp_2022 = 0
    for i in range(20+365+18+365+17, 20+365+18+365+17+365):
        data = root[i][0].text.split(' ')
        if(len(data) == 3):
            root[i].attrib['fill'] = get_color(int(data[1]))
            print(data[0],data[1]+"XP")
            sum_xp_2022 += int(data[1])

    # 2023 year data output
    sum_xp_2023 = 0
    for i in range(20+365+18, 20+365+18+365):
        data = root[i][0].text.split(' ')
        if(len(data) == 3):
            root[i].attrib['fill'] = get_color(int(data[1]))
            print(data[0],data[1]+"XP")
            sum_xp_2023 += int(data[1])

    # 2024 year data output, support check and append data
    sum_xp_2024 = 0
    for i in range(20, 20+365):
        data = root[i][0].text.split(' ')
        if(len(data) == 3):
            root[i].attrib['fill'] = get_color(int(data[1]))
            print(data[0],data[1]+"XP")
            sum_xp_2024 += int(data[1])
        if(len(data) == 1):
            if(time.strptime(data[0], "%Y-%m-%d") < time.localtime()):
                if(time.strftime("%Y-%m-%d", time.localtime()) != data[0]):
                    print(data[0],"not dat available!")
                    if(len(append_list) != 0):
                        for j in range(0, len(append_list)):
                            if(append_list[j][0] == data[0]):
                                root[i][0].text = data[0]+" "+str(append_list[j][1])+" XP"
                                root[i].attrib['fill'] = get_color(append_list[j][1])
                                sum_xp_2024 += append_list[j][1]
    
    print("sum_xp_2022:", sum_xp_2022, "svg:" ,root[4+365+18+365+17].text)
    print("sum_xp_2023:", sum_xp_2023, "svg:" ,root[4+365+18].text)
    print("sum_xp_2024:", sum_xp_2024, "svg:" ,root[4].text)
    if(root[4].text != str(sum_xp_2024)+" XP"):
        root[4].text = str(sum_xp_2024)+" XP"

    xml.write(file_or_filename=svg_file, encoding="utf-8", xml_declaration=None, default_namespace=None, method="xml")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 parse_duolingo_svg.py svg_file")
        sys.exit(1)
    svg_file = sys.argv[1]
    parse_svg(svg_file)

