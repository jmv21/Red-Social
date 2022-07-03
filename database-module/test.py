import uuid

from DB import *


db = db_connect()

user_register('carlos', 'name', uuid.uuid4().int & (1 << 63) - 1)
user_register('jose', 'name', uuid.uuid4().int & (1 << 63) - 1)
user_register('david', 'name', uuid.uuid4().int & (1 << 63) - 1)
user_register('charles', 'name', uuid.uuid4().int & (1 << 63) - 1)

# tweet(get_id_by_name('carlos'), "Hola soy {}".format('Carlos'))
# tweet(get_id_by_name('jose'), "Hola soy {}".format('jose'))
# tweet(get_id_by_name('david'), "Hola soy {}".format('david'))
# tweet(get_id_by_name('charles'), "Hola soy {}".format('charles1'))
# tweet(get_id_by_name('charles'), "Hola soy {}".format('charles2'))
# tweet(get_id_by_name('charles'), "Hola soy {}".format('charles3'))
# tweet(get_id_by_name('charles'), "Hola soy {}".format('charles4'))
# tweet(get_id_by_name('charles'), "Hola soy {}".format('charles5'))
# tweet(get_id_by_name('charles'), "Hola soy {}".format('charles6'))
# tweet(get_id_by_name('charles'), "Hola soy {}".format('charles7'))
# tweet(get_id_by_name('charles'), "Hola soy {}".format('charles8'))
# tweet(get_id_by_name('charles'), "Hola soy {}".format('charles9'))
# tweet(get_id_by_name('charles'), "Hola soy {}".format('charles10'))
# tweet(get_id_by_name('charles'), "Hola soy {}".format('charles11'))
#
# follow(get_id_by_name('carlos'), get_id_by_name('david'))
# follow(get_id_by_name('carlos'), get_id_by_name('charles'))

friends = get_friends(get_id_by_name('carlos'))
result = get_followed_updated_tweets(friends)

for element in result:
    for item in element[1]:
        print(item['content'])

