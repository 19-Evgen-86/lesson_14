import sqlite3

from collections import Counter


def get_from_sql(sql_query):
    with sqlite3.connect("netflix.db") as db:
        db.row_factory = sqlite3.Row
        return db.execute(sql_query).fetchall()


def search_by_title(title: str):
    sql_query = f"select `title`,`country`,`release_year`,`listed_in`,`description` " \
                f"from netflix " \
                f"where lower (`title`)= lower('{title}')" \
                f"and type = 'Movie' " \
                f"order by `release_year` desc  " \
                f"limit 1 "

    if get_from_sql(sql_query):
        for item in get_from_sql(sql_query):
            return dict(item)
    else:
        return f"фильм '{title}' в базе не найден!"


def search_year_to_year(start: int, end: int):
    result = []
    sql_query = f"select `title`,`release_year` " \
                f"from netflix " \
                f"where `release_year` between '{start}' and '{end}' " \
                f"order by `release_year` " \
                f"limit 100"

    response_sql = get_from_sql(sql_query)

    for item in response_sql:
        result.append(dict(item))
    return result


def search_by_rating(rating: str):
    rating_list = []
    result = []

    if rating == "children":
        rating_list = ['G']
    elif rating == "family":
        rating_list = ['G', 'PG', 'PG-13']
    elif rating == 'adult':
        rating_list = ['R', 'NC-17']

    sql_query = f"select `title`,`rating`,`description` " \
                f"from netflix " \
                f"where `rating` in {tuple(x for x in rating_list)} " \
                f"order by `release_year` desc "

    response_sql = get_from_sql(sql_query)
    for item in response_sql:
        result.append(dict(item))

    return result


def search_by_genre(genre: str):
    result = []
    sql_query = f"select `title`,`description` " \
                f"from netflix " \
                f"where lower(`listed_in`) like lower('%{genre}%') " \
                f"order by `release_year` desc "

    response_sql = get_from_sql(sql_query)
    for item in response_sql:
        result.append(dict(item))

    return result


def search_by_casts(input_names: list):
    """
    Напишите функцию, которая получает в качестве аргумента имена двух актеров, сохраняет всех актеров из колонки cast
    и возвращает список тех, кто играет с ними в паре больше 2 раз.
    В качестве теста можно передать: Rose McIver и Ben Lamb, Jack Black и Dustin Hoffman.
    :param actors:
    :return:
    """
    sql_query = f"select `cast` " \
                f"from netflix " \
                f"where `cast` != '' "

    response_sql = get_from_sql(sql_query)
    # преобразуем изначальный список актеров в множество
    actors_input = set(name.lower() for name in input_names)
    # список актеров, которые играют с заданными актерам
    actors_list = []
    # список актеров, которые играют с заданными актерам в паре больше 2 раз
    actors_result = []

    for item in response_sql:
        # создаем список актеров из БД в виде множества
        actors = set(actor.lower() for actor in list(item)[0].split(', '))

        # если имена выбранных актеров присутствуют в итерируемом множества(список актеров фильма из БД)
        if actors_input.issubset(actors):
            # добавляем в результирующий список(вычитанием множеств убираем заданных актеров)
            actors_list.extend(actors - actors_input)

    # используем функцию Counter из collections для подсчета количества повторяющихся элементов
    for actor, count in Counter(actors_list).items():
        if count > 2:
            actors_result.append(actor)

    print(actors_result)


def get_data_by_param(data: list):
    """
    Напишите функцию, с помощью которой можно будет передавать **тип** картины (фильм или сериал), **год выпуска**
    и ее **жанр** и получать на выходе список названий картин с их описаниями в JSON.
    :return:
    """
    type_film, release_year, ganre = data

    result = []
    sql_query = f"select `title`,`description` " \
                f"from netflix " \
                f"where `type` = '{type_film}'" \
                f"and `release_year`= '{release_year}' " \
                f"and `listed_in` like '%{ganre}%'"

    response_sql = get_from_sql(sql_query)

    for item in response_sql:
        result.append(dict(item))

    print(result)


# search_by_casts(['Rose McIver', 'Ben Lamb'])
# search_by_casts(['Jack Black', 'Dustin Hoffman'])
# get_data_by_param(['Movie', 2017, 'Children'])
