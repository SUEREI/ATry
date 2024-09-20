import requests
import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as mbox
import time

global file_name, data_list_choose
file_name = './'


# 生成时间戳
def generate_timestamp():
    return str(int(time.time() * 1000))


# 获取网站数据
def get_html(u):
    if engine.get() == 'baidu':
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
        }
    elif engine.get() == 'sogou':
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Connection": "keep-alive",
            "Host": "image.sogou.com",
            "Sec-Ch-Ua": '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0"
        }
    else:
        pass
    # 异常处理
    try:
        this_time = generate_timestamp()
        headers["X-Time4p"] = this_time
        r = requests.get(u, headers=headers)
        r.raise_for_status()
        json_data = r.json()
        if engine.get() == 'baidu':
            return json_data['data']
        elif engine.get() == 'sogou':
            return json_data['data']['items']
        else:
            pass
    except:
        return '访问异常'


# 获取图片数据
def get_soup(u, page):
    global file_name, data_list_choose
    data_list = get_html(u)
    num = 1
    if engine.get() == 'baidu':
        data_list_choose = data_list[:-1]
    elif engine.get() == 'sogou':
        data_list_choose = data_list
    else:
        pass
    for data in data_list_choose:
        try:
            if engine.get() == 'baidu':
                # fromPageTitle = data['fromPageTitle']
                middleURL = data['middleURL']
                # print(fromPageTitle, middleURL)
            elif engine.get() == 'sogou':
                middleURL = data['locImageLink']
            img_data = requests.get(middleURL).content
            with open(file_name + f'/{engine.get()}-{entry_1.get()}-{page+1}-{num}.jpg', 'wb') as f:
                f.write(img_data)
                text_1.insert('end', f'正在采集第{page+1}/{int(entry_2.get())}页，第{num}/{len(data_list_choose)}张图片,累计采集{page*len(data_list_choose)+num}张图片\n')
                text_1.update()
                text_1.see('end')
                # print(f'正在采集第{page}/{int(entry_2.get())}页，第{num}/{len(data_list[:-1])}张图片,累计采集{(page-1)*len(data_list[:-1])+num}张图片')
            num = num + 1
        except:
            continue


def start():
    global file_name, data_list_choose
    if file_name != r'./':
        for page in range(0, int(entry_2.get())):
            kw = entry_1.get()
            if engine.get() == 'baidu':
                label_4.config(text='当前搜索引擎为百度，采集结果：')
                url = (
                    f'https://image.baidu.com/search/acjson?tn=resultjson_com&logid=10439630927142435712&ipn=rj&ct=201326592&is=&fp=result&fr=&word={kw}&queryWord=jk&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=&z=&ic=&hd=&latest=&copyright=&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=1&expermode=&nojc=&isAsync=&pn={page * 30}&rn=30&gsm=96&1723278007439=')
            elif engine.get() == 'sogou':
                label_4.config(text='当前搜索引擎为搜狗，采集结果：')
                url = (
                    f'https://image.sogou.com/napi/pc/searchList?mode=1&start={page * 48}&xml_len=48&query={kw}&channel=pc_pic&scene=pic_result'
                )
            else:
                mbox.showwarning('提示', '未选择搜索引擎')
            get_soup(url, page)
            # print(url)
        mbox.showwarning('采集报告', f'采集完成！共采集{int(entry_2.get()) * len(data_list_choose)}张图片')
    else:
        mbox.showwarning('警告', '未选择保存路径')


def callback():
    global file_name
    file_name = fd.askdirectory()
    return file_name


# GUI编程
root = tk.Tk()
root.title('图片爬取')
# root.geometry('500x500')

# 定义控件
label_1 = tk.Label(root, text='采集关键词：')
label_2 = tk.Label(root, text='采集页面数：')
entry_1 = tk.Entry(root)
entry_2 = tk.Entry(root)
engine = tk.StringVar()
radiobutton_1 = tk.Radiobutton(root, text='百度', variable=engine, value='baidu')
radiobutton_2 = tk.Radiobutton(root, text='搜狗', variable=engine, value='sogou')
btn_1 = tk.Button(root, text='保存路径', command=callback)
btn_2 = tk.Button(root, text='开始采集', command=start)
label_3 = tk.Label(root, text='#百度一页图片30张、搜狗一页图片48张')
label_ = tk.Label(root, text='-----------------------------------------------------')
label_4 = tk.Label(root, text='采集结果：')
text_1 = tk.Text(root, height=5, width=50)

# 布局控件
label_1.grid(row=0, column=0, sticky='w')
label_2.grid(row=1, column=0, sticky='w')
entry_1.grid(row=0, column=1)
entry_2.grid(row=1, column=1)
radiobutton_1.grid(row=0, column=2)
radiobutton_2.grid(row=1, column=2)
btn_1.grid(row=0, column=3, sticky=tk.E)
btn_2.grid(row=1, column=3, sticky=tk.E)
label_3.grid(row=2, column=0, columnspan=4)
label_.grid(row=3, column=0, columnspan=4)
label_4.grid(row=4, column=0, columnspan=4, sticky=tk.W)
text_1.grid(row=5, column=0, columnspan=4)

root.mainloop()