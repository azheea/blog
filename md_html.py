import markdown
import os

# 将Markdown文本转换为HTML
def read_all_passages() -> dict:
    files = os.listdir("./passages")
    passages = {}
    for file in files:
        with open(f"./passages/{file}", "r", encoding="utf-8") as f:
            passage = file[:len(file)-3]
            passage_date = (passage.split("-"))[0]
            passage_name = (passage.split("-"))[1]
            passages[passage_name] = [passage_date,markdown.markdown(f.read())]
            # print(passage)
    # print(passages)
    return passages
# print(read_all_passages())