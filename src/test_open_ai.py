from typing import Union

import openai as oa
from data_parser import extract_context_from_file
from src.dbutils import read_context, get_secret

oa.api_key = get_secret("OPENAI_KEY")
MAX_TEXT_LENGTH = 4095


def chat_bot_cold_start():
    """
    Initializes context of the bot using data from text file and recorded interactions in the database
    :return:
    """

    messages = [
        {"role": "system",
         "content": "Ты умный бот телеграмм группы gpt_web3_hackathon. Твоя задача помочь участникам группы получить информацию о LATOKEN и хакатоне организованном этой компанией. Также при необходимости ты должен уметь проверять переданные пользователям знания с помощью интерактивного теста с вариантами ответов."},
        {"role": "system", "content": "Информация о LATOKEN:"},
        # {"role": "assistant", "content": "relevant: farts exert force"},  # RAG
        # {"role": "user", "content": "Do penguin farts propel?"}
    ]
    messages.extend(extract_context_from_file("../data/cold_start_data.txt"))
    prev_context = read_context()
    for interaction in prev_context:
        messages.append(
            {"role": interaction[0], "content": interaction[1], "name": interaction[2]}
        )
    return messages


MESSAGES = chat_bot_cold_start()


def get_gpt_answer() -> Union[str, list[str]]:
    """
    Gets answer from chat-GPT and split it if it is too long
    model param to create can be gpt-3.5-turbo or gpt-4o or others
    :return: eaither a string or a list of strings
    """
    cc = oa.chat.completions.create(
        messages=MESSAGES, max_tokens=4096, top_p=.69, model="gpt-4o")
    answer = cc.choices[0].message.content
    if len(answer) > MAX_TEXT_LENGTH:
        answer = [answer[i:i + MAX_TEXT_LENGTH] for i in range(0, len(answer), MAX_TEXT_LENGTH)]
    return answer


if __name__ == '__main__':

    chat_bot_cold_start()
    MESSAGES.append(
        {"role": "user", "content": "Что такое LATOKEN?"}
    )
    ans = get_gpt_answer()

    print(ans)
    MESSAGES.append(
        {"role": "user", "content": "Раскажи о хакатоне LATOKEN"}
    )
    ans = get_gpt_answer()
    print(ans)
