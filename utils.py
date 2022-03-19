import sqlite3

from collections import Counter


def get_from_sql(sql_query):
    with sqlite3.connect("netflix.db") as db:
        cursor = db.cursor()
        return cursor.execute(sql_query).fetchall()


def search_by_title(title: str):
    sql_query = f"select `title`,`country`,`release_year`,`listed_in`,`description` " \
                f"from netflix " \
                f"where lower (`title`)= lower('{title}')" \
                f"and type = 'Movie' " \
                f"order by `release_year` desc  " \
                f"limit 1 "

    if get_from_sql(sql_query):

        return {
            "title": get_from_sql(sql_query)[0][0],
            "country": get_from_sql(sql_query)[0][1],
            "release_year": get_from_sql(sql_query)[0][2],
            "genre": get_from_sql(sql_query)[0][3],
            "description": get_from_sql(sql_query)[0][4].rstrip('\n')
        }

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
        result.append({'title': item[0], 'release_year': item[1]})

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
        result.append({
            "title": item[0],
            "rating": item[1],
            "description": item[2].rstrip('\n')
        })

    return result


def search_by_genre(genre: str):
    result = []
    sql_query = f"select `title`,`description` " \
                f"from netflix " \
                f"where lower(`listed_in`) like lower('%{genre}%') " \
                f"order by `release_year` desc "

    response_sql = get_from_sql(sql_query)
    for item in response_sql:
        result.append({
            "title": item[0],
            "description": item[1].rstrip('\n')
        })

    return result


def search_by_casts(actors: list):
    """
    Напишите функцию, которая получает в качестве аргумента имена двух актеров, сохраняет всех актеров из колонки cast
    и возвращает список тех, кто играет с ними в паре больше 2 раз.
    В качестве теста можно передать: Rose McIver и Ben Lamb, Jack Black и Dustin Hoffman.
    :param actors:
    :return:
    """
    sql_query = f"select lower (`cast`) " \
                f"from netflix " \
                f"where `cast` != '' "

    response_sql = get_from_sql(sql_query)

    actors_1 = actors[0].lower().strip()
    actors_2 = actors[1].lower().strip()
    # список актеров, которые играют с заданными актерам в паре больше 2 раз
    actors_result = []
    # список актеров, которые играют с заданными актерам
    actors_list = []

    for item in response_sql:
        if actors_1 in item[0] and actors_2 in item[0]:
            actors = [actor.strip() for actor in item[0].split(',') if
                      actor.strip() != actors_1 and actor.strip() != actors_2]

            actors_list.extend(actors)

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
        result.append({
            "title": item[0],
            "description": item[1].rstrip('\n')
        })

    print(result)


# search_by_casts(['Rose McIver', 'Ben Lamb'])
# search_by_casts(['Jack Black', 'Dustin Hoffman'])
get_data_by_param(['Movie', 2017, 'Children'])
