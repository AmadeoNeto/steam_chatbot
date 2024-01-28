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
