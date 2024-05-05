from flask import Flask, render_template
import md_html
import json
import re

with open("config.json", encoding="utf-8") as configs:
    config = json.load(configs)

app = Flask(__name__, static_url_path='/')

@app.route("/")
def page1():
    return index(1)

@app.route("/<int:page>")
def index(page):
    all_passages = md_html.read_all_passages()
    passage_num = len(all_passages)
    passage_show = {}
    def process():
            title = list(all_passages.keys())[(page - 1) * 5 + i]
            content = all_passages.get(title)[1]
            # 使用正则表达式消除 HTML 代码
            content_without_html = re.sub(r'<[^>]+>', '', content)
            content_without_html = re.sub(r'\n', ' ', content_without_html)
            # 删除前 20 个字符
            content_shortened = content_without_html[:20]
            passage_show[title] = content_shortened
            
    #选择要展示的文章
    if passage_num >= page * 5:
        for i in range(5):
            process()
    elif passage_num >= (page - 1) * 5:
        for i in range(passage_num - ((page - 1) * 5)):
            process()
    else:
        return render_template("./404.html",
                               title=f"{config['title']} | 走丢了",
                               favicon=config["favicon"],
                               background=config["background"],
                               )
    return render_template("./index.html",
                           title=f"{config['title']} | 主页",
                           favicon=config["favicon"],
                           background=config["background"],
                           passages=passage_show
                           )


@app.route("/blog/<blog>")
def show_blog(blog):
    passages = md_html.read_all_passages()
    content = passages.get(blog, "404")
    if content != "404":
        # 将换行符替换为 <br> 标签
        content_with_br = re.sub(r'\n', '<br>', content[1])
        return render_template("./blog.html",
                               title=f"{config['title']} | {blog}",
                               favicon=config["favicon"],
                               background=config["background"],
                               post_title=blog,
                               post_date=content[0],
                               post_content=content_with_br,  # 使用处理过的内容
                               )
    else:
        return render_template("404.html"), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000)