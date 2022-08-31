import pandas as pd

df = pd.read_csv('test_data1.csv')


def talks_parsing(csv_file):  # Делим все разговоры по номеру диалога и добавляем по словарю - ключ номер диалога, диалог - словарь (диалоги менеджера)
    talk_list = []
    talk_dict = {}
    start_number_talk = 0
    try:
        for dlg in csv_file.loc:
            if dlg['role'] == 'manager':
                if dlg['dlg_id'] == start_number_talk:
                    talk_list.append(dlg['text'])
                else:
                    talk_dict[start_number_talk] = talk_list
                    talk_list = []
                    talk_list.append(dlg['text'])
                    start_number_talk += 1
        return talk_dict
    except Exception:
        talk_dict[start_number_talk] = talk_list
        return talk_dict


def dlg_manager_dl(talk_dict, frst_find_word, tw_find_word):  # Поиск в диалогах менеджеров по ключевому слову (двум)
    request_list = []
    talk_number = 1
    for tlk in range(len(talks_parsing(df))):
        for i in talk_dict[tlk]:
            if frst_find_word in i.lower():
                request_list.append(
                    f'В разговоре №{talk_number} (dlg_id №{talk_number - 1}) менеджер поприветствовал (фраза "{i}")')
                break
            elif tw_find_word in i.lower():
                request_list.append(
                    f'В разговоре №{talk_number} (dlg_id №{talk_number - 1}) менеджер поприветствовал (фраза "{i}")')
                break
        talk_number += 1
    return request_list


def dlg_manager(talk_dict, find_word):  # Поиск в диалогах менеджеров по ключевому слову
    request_list = []
    talk_number = 1
    for tlk in range(len(talks_parsing(df))):
        for i in talk_dict[tlk]:
            if find_word in i.lower():
                request_list.append(
                    f'В разговоре №{talk_number} (dlg_id №{talk_number - 1}) менеджер представляется (фраза "{i}")\n Имя менеджера: {i.split(find_word)[1].split()[0]}')
                break
        talk_number += 1
    return request_list


def manager_wrong(hello_list, bye_list):
    manager_say_hello = []
    manager_say_bey = []
    manager_say_hello_bey = []
    manager_not_ay_hello_bey = []
    returned_list = []
    for i in hello_list:
        manager_say_hello.append(i.split('№')[1].split()[0])
    for i in bye_list:
        manager_say_bey.append(i.split('№')[1].split()[0])
    for number in manager_say_hello:
        if number in manager_say_bey:
            manager_say_hello_bey.append(number)
    for i in manager_say_hello:
        if i not in manager_say_bey:
            manager_not_ay_hello_bey.append(i)
    for i in manager_say_bey:
        if i not in manager_say_hello:
            manager_not_ay_hello_bey.append(i)
    returned_list.append(manager_say_hello_bey)
    returned_list.append(manager_not_ay_hello_bey)
    return returned_list

print('Приветствие менеджеров:')
for i in dlg_manager_dl(talks_parsing(df), 'здравствуйте', 'добрый'):
    print(i)

print('\nПредставление и имена менеджеров:')
for i in dlg_manager(talks_parsing(df), 'зовут'):
    print(i)

print('\nНазвание компании:')
for i in dlg_manager(talks_parsing(df), 'компания'):
    print(i)

print('\nМенеджер попращался:')
for i in dlg_manager_dl(talks_parsing(df), 'до свидания', 'всего доброго'):
    print(i)

print('\nМенеджер не нарушил требование (представление и/или прощание) в разговоре № ', end='')
for i in manager_wrong(dlg_manager_dl(talks_parsing(df), 'здравствуйте', 'добрый'), dlg_manager_dl(talks_parsing(df), 'до свидания', 'всего доброго'))[0]:
    print(f"{i} (dlg_id №{int(i) - 1})", end='; ')
print('\nСоответственно, нарушил требование (представление и/или прощание) в разговоре № ', end='')
for i in manager_wrong(dlg_manager_dl(talks_parsing(df), 'здравствуйте', 'добрый'), dlg_manager_dl(talks_parsing(df), 'до свидания', 'всего доброго'))[1]:
    print(f"{i} (dlg_id №{int(i) - 1})", end='; ')