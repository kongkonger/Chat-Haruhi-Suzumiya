import zipfile
import gradio as gr
from PIL import Image
from chatharuhi import ChatHaruhi
import wget
import os
import openai



NAME_DICT = {'汤师爷': 'tangshiye', '慕容复': 'murongfu', '李云龙': 'liyunlong', 'Luna': 'Luna', '王多鱼': 'wangduoyu',
             'Ron': 'Ron', '鸠摩智': 'jiumozhi', 'Snape': 'Snape',
             '凉宫春日': 'haruhi', 'Malfoy': 'Malfoy', '虚竹': 'xuzhu', '萧峰': 'xiaofeng', '段誉': 'duanyu',
             'Hermione': 'Hermione', 'Dumbledore': 'Dumbledore', '王语嫣': 'wangyuyan',
             'Harry': 'Harry', 'McGonagall': 'McGonagall', '白展堂': 'baizhantang', '佟湘玉': 'tongxiangyu',
             '郭芙蓉': 'guofurong', '旅行者': 'wanderer', '钟离': 'zhongli',
             '胡桃': 'hutao', 'Sheldon': 'Sheldon', 'Raj': 'Raj', 'Penny': 'Penny', '韦小宝': 'weixiaobao',
             '乔峰': 'qiaofeng', '神里绫华': 'ayaka', '雷电将军': 'raidenShogun', '于谦': 'yuqian'}


def get_response(user_name, user_text, role, chatbot):
    # 下载role zip 并解压
    role_en = NAME_DICT[role]
    if not os.path.exists("characters_zip"):
        os.makedirs("characters_zip")
    if not os.path.exists("characters"):
        os.makedirs("characters")
    if NAME_DICT[role] not in os.listdir("./characters"):
        file_url = f"https://github.com/LC1332/Haruhi-2-Dev/raw/main/data/character_in_zip/{role_en}.zip"
        os.makedirs(f"characters/{role_en}")
        destination_file = f"characters_zip/{role_en}.zip"
        wget.download(file_url, destination_file)
        destination_folder = f"characters/{role_en}"
        with zipfile.ZipFile(destination_file, 'r') as zip_ref:
            zip_ref.extractall(destination_folder)

    db_folder = f"./characters/{role_en}/content/{role_en}"
    system_prompt = f"./characters/{role_en}/content/system_prompt.txt"
    haruhi = ChatHaruhi(system_prompt=system_prompt,
                        llm="openai",
                        story_db=db_folder,
                        verbose=True)
    response = haruhi.chat(role=user_name, text=user_text)
    chatbot.append((user_text, response))
    return chatbot


def clear(user_name, user_text, chatbot):
    return None, None, []


def get_image(role):
    role_en = NAME_DICT[role]
    return Image.open(f'images/{role_en}.jpg'), None, None, []


with gr.Blocks() as demo:
    gr.Markdown(
        """
        # Chat凉宫春日 ChatHaruhi
        ## Reviving Anime Character in Reality via Large Language Model
        
        ChatHaruhi2.0的demo implemented by [chenxi](https://github.com/todochenxi)
        
        更多信息见项目github链接 [https://github.com/LC1332/Chat-Haruhi-Suzumiya](https://github.com/LC1332/Chat-Haruhi-Suzumiya)
        
        如果觉得有趣请拜托为我们点上star. If you find it interesting, please be kind enough to give us a star.
        
        user_role 为角色扮演的人物 请尽量设置为与剧情相关的人物 且不要与主角同名
        """
    )
    with gr.Row():
        chatbot = gr.Chatbot()
        role_image = gr.Image(height=400, value="./images/haruhi.jpg")
    with gr.Row():
        user_name = gr.Textbox(label="user_role")
        user_text = gr.Textbox(label="user_text")
    with gr.Row():
        submit = gr.Button("Submit")
        clean = gr.ClearButton(value="Clear")
    role = gr.Radio(['汤师爷', '慕容复', '李云龙',
                     'Luna', '王多鱼', 'Ron', '鸠摩智',
                     'Snape', '凉宫春日', 'Malfoy', '虚竹',
                     '萧峰', '段誉', 'Hermione', 'Dumbledore',
                     '王语嫣',
                     'Harry', 'McGonagall',
                     '白展堂', '佟湘玉', '郭芙蓉',
                     '旅行者', '钟离', '胡桃',
                     'Sheldon', 'Raj', 'Penny',
                     '韦小宝', '乔峰', '神里绫华',
                     '雷电将军', '于谦'], label="characters", value='凉宫春日')
    role.change(get_image, role, [role_image, user_name, user_text, chatbot])
    user_text.submit(fn=get_response, inputs=[user_name, user_text, role, chatbot], outputs=[chatbot])
    submit.click(fn=get_response, inputs=[user_name, user_text, role, chatbot], outputs=[chatbot])
    clean.click(clear, [user_name, user_text, chatbot], [user_name, user_text, chatbot])
demo.launch(debug=True)
