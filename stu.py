import time
import requests
from bs4 import BeautifulSoup
import random
import os
import html2text

# 请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# URL地址集
urls = [
    'https://kidscodes.cn/10283.html',
    'https://kidscodes.cn/3224.html',
]
divs = [
    'b',
    'img',
    'video'
]

class_ = [
    'post-views-label',
    'post-views-count'
]

# 遍历每个URL
for url in urls:
    # 发送请求
    response = requests.get(url, headers=headers)
    
    # 检查请求是否成功
    if response.status_code == 200:
        # 解析页面
        soup = BeautifulSoup(response.content, "html.parser")
        
        # 获取指定ID的div
        div_id = "entry-content"
        div_content = soup.find("div", {'class': div_id})

        if div_content:
            
            # 清空指定标签内容
            for v in divs:
                div_tags = div_content.find_all({v})
                for tag in div_tags:
                    tag.decompose()  # 清空标签内容，但保留标签本身
                print(f"已成功清空 {len(div_tags)} 个 {v} 标签的内容")
            
            # 去除指定class所在标签内容
            for v2 in class_:
                class_tags = div_content.find_all(class_ = {v2})
                for tag2 in class_tags:
                    tag2.decompose()  # 清空标签内容，但保留标签本身
                print(f"已成功清空 {len(class_tags)} 个 {v2} 标签的内容")

            # 转换为字符串
            div_content_str = html2text.html2text(str(div_content))
            
            # 获取文章标题
            title = soup.title.string.strip() if soup.title else "default_title"
            
            # 生成随机数
            random_value = random.randint(10000, 99999)  # 生成一个5位的随机数
            
            # 构建文件名
            filename = f"{title}_{random_value}.md"
            
            # 确保文件名符合操作系统的要求
            filename = os.path.basename(filename)
            
            # 写入文件
            try:
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(div_content_str)
                print(f"内容已成功保存到文件: {filename}")
            except Exception as e:
                print(f"写入文件时出错: {e}")
        else:
            print(f"未找到class为 {div_id} 的<div>元素")
        
    else:
        print(f"请求失败，状态码：{response.status_code}")
    
    # 每次请求后休眠2秒
    time.sleep(2)