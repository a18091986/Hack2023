import pandas as pd
import pickle as pkl


def filter_cols_data(data, col, m):
    '''Функция для фильтрации датасета'''
    woman = data[['line_3', 'id_level3', 'markup']][data['gender'] == col].groupby(['id_level3','markup'])['line_3']\
        .count()\
        .reset_index()\
        .sort_values(by='line_3', ascending=False)
    woman_body = woman[woman['markup'] == 'Для тела']
    woman_soul = woman[woman['markup'] == 'Для души']
    woman_mind = woman[woman['markup'] == 'Для ума']
    woman_list_body = list(woman_body['id_level3'].head(m))
    woman_list_soul = list(woman_soul['id_level3'].head(m))
    woman_list_mind = list(woman_mind['id_level3'].head(m))

    return woman_list_body, woman_list_soul, woman_list_mind


def my_popularity_recommendation(data, n=12):
    """Топ-n популярных товаров """
    '''Возвращает id для 3-го направления занятий(id_level3)'''

    recs = []

    # Рекомендации для женщин
    woman_list_body, woman_list_soul, woman_list_mind = filter_cols_data(data, 'Женщина', m=n)
    # Дополняем общий список рекомендациями для женщин, исключаем повторяющиеся рекомендации
    i = 0

    while len(recs) < round(n * 0.7):
        if woman_list_body[i] or woman_list_soul[i] or woman_list_mind[i] not in recs:
            if i % 3 == 0 and i != 0:
                recs.append(woman_list_body[i])
            elif i % 2 == 0:
                recs.append(woman_list_soul[i])
            elif i % 2 != 0:
                recs.append(woman_list_mind[i])
        i += 1

    # Рекомендации для мужчин

    man_list_body, man_list_soul, man_list_mind = filter_cols_data(data, 'Мужчина', m=n)

    # Дополняем общий список рекомендациями для мужчин, исключаем повторяющиеся рекомендации

    j = 0

    while len(recs) < n:
        if man_list_body[j] or man_list_soul[j] or man_list_mind[j] not in recs:
            if j % 3 == 0 and i != 0:
                recs.append(man_list_body[j])
            elif j % 2 == 0:
                recs.append(man_list_soul[j])
            elif j % 2 != 0:
                recs.append(man_list_mind[j])
        j += 1

    return recs


if __name__ == '__main__':
    top_recs = []
    df = pd.read_csv('datasets_prep/result.csv')
    list_rec = my_popularity_recommendation(df)
    for i in list_rec:
        # print(df['line_3'][df['id_level3'] == i].head(1).reset_index().values.tolist()[0])
        top_recs.append(df['line_3'][df['id_level3'] == i].head(1).reset_index().values.tolist()[0][1])
    print(top_recs)
    with open('serialize/top_recs.pkl', 'wb') as f:
        pkl.dump(top_recs, f)
