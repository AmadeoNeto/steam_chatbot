import pandas as pd

def query_builder(genres=None,
                    platforms=None,
                    developer=None,
                    categories=None,
                    release_date=None,
                    game_tag=None):
    query = 'SELECT * FROM game_info WHERE'

    conditions = []

    if game_tag:
        conditions.append(' AND '.join(['steamspy_tags LIKE \'%{}%\''.format(tag) for tag in game_tag]))

    if genres:
        conditions.append(' AND '.join(['genres LIKE \'%{}%\''.format(genre) for genre in genres]))

    if platforms:
        conditions.append(' AND '.join(['platforms LIKE \'%{}%\''.format(platform) for platform in platforms]))

    if developer:
        conditions.append(f'(developer LIKE \'%{developer}%\' OR publisher LIKE \'%{developer}%\')')

    if categories:
        conditions.append(' AND '.join(['categories LIKE \'%{}%\''.format(category) for category in categories]))

    if release_date:
        conditions.append('release_date LIKE \'%{}%\''.format(release_date))

    if conditions:
        query += ' AND '.join(['(' + condition + ')' for condition in conditions])

    query += '\nAND positive_ratings = (SELECT MAX(positive_ratings) FROM game_info'

    if conditions:
        query += ' WHERE '
        query += ' AND '.join(['(' + condition + ')' for condition in conditions])

    query += ')'

    return query
    

def generate_context_string(row):
    return ' | '.join([f"{col}: {val}" for col, val in row.items()])


def generate_qa_context(game_title, connection):
    query = f'''SELECT gi.name, gi.release_date, gi.developer, gi.publisher, gi.platforms,
           gi.categories, gi.genres, gi.steamspy_tags, gi.price, d.short_description 
           FROM description d, game_info gi 
           WHERE d.steam_appid = gi.appid
           AND gi.name LIKE \'%{game_title}%\' '''
    

    result_df = pd.read_sql_query(query, connection)

    # Apply the function to each row and concatenate the results
    if len(result_df) > 0:
        context = result_df.apply(generate_context_string, axis=1)
        context = context.values[0]
    else:
        context = ""

    return context

import sqlite3
path_to_game_info_db = r"C:\Users\Amadeo\Documents\_UFPE\Eletivas\PLN\chatbot\steam_chatbot\steam_base.db"
conn = sqlite3.connect(path_to_game_info_db)
print(generate_qa_context(None,conn))