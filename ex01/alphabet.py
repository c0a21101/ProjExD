import random
import string
import datetime

TARGET_AMT = 10
DELETE_AMT = 2
MAX_ANSWER = 3

def target():
    alphabet = random.sample(string.ascii_uppercase, TARGET_AMT)
    print("対象文字：")
    print(*alphabet)
    return alphabet


def delete(target_lst):
    random.shuffle(target_lst)
    delete_lst = target_lst[:DELETE_AMT]
    remain_lst = target_lst[DELETE_AMT:]
    print("欠損文字：")
    print(*delete_lst)
    print("表示文字：")
    print(*remain_lst)
    return delete_lst


def answer(delete_lst):
    if int(input("欠損文字はいくつあるでしょうか？")) == DELETE_AMT:
        print("正解です。それでは、具体的に欠損文字を1つずつ入力してください")
        ans_list = []
        for i in range(DELETE_AMT):
            ans_list.append(input(f"{i+1}番目の文字を入力してください："))
        if sorted(ans_list) == sorted(delete_lst):
            return True
        else:
            return False
    else:
        return False

            
if __name__ == "__main__":
    st = datetime.datetime.now()
    for _ in range(MAX_ANSWER):
        target_lst = target()
        delete_lst = delete(target_lst)
        if answer(delete_lst) == True:
            print("正解です。おめでとうございます。")
            break
        else:
            print("不正解です。")
            print("-" * 20)
    else:
        print("解答権がなくなりました。残念！w")
    ed = datetime.datetime.now()
    print("実行時間：" + str((ed - st).seconds) + "秒")