import config
from datetime import datetime
import MySQLdb
import traceback


_connected = False
_database = None
_cursor = None

# setupConnection() must be called before anything else for this to work
# closeConnection() should be called after finishing


def setupConnection():
    global _connected
    global _database
    global _cursor

    if not _connected:
        try:
            _database = MySQLdb.connect(host="localhost",
                                        user="root",
                                        passwd=config.password,
                                        db="gttravel")
            _cursor = _database.cursor()
            _connected = True
        except Exception as e:
            _connected = False
            traceback.print_exc()


def closeConnection():
    global _connected

    if _connected:
        _database.close()
        _connected = False


# returns 1 if username is taken
# returns 2 if email is taken
# returns 0 if insert was valid
# returns 3 if everything is screwed
def register(username, email, password, ismanager):
    query = "INSERT INTO users(Username, Email, Password, Is_manager)"\
            "VALUES (%s, %s, %s, %s);"
    try:
        response = _cursor.execute(query, (username, email, password, ismanager))
        _database.commit()

        return 0
    except Exception as e:
        if e[1][-2:] == 'Y\'':  # violates primary key constraint, username
            return 1
        elif e[1][-2:] == 'l\'':  # violates email uniqueness constraint
            return 2
        else:  # don't get here
            return 3


# returns 0 if credentials are invalid
# returns 1 if user is a manager
# returns 2 if user is NOT a manager
def login(username, password):
    query = "SELECT * FROM users WHERE Username = %s AND Password = %s;"
    response = _cursor.execute(query, (username, password))

    # clear cursor
    _cursor.fetchall()

    if response == 0:
        return 0
    else:
        query = "SELECT Is_manager FROM users WHERE Username = %s;"
        response = _cursor.execute(query, (username,))

        result = _cursor.fetchone()

        # sanity check
        _cursor.fetchall()

        if result[0] == 1:  # if Is_manager
            return 1
        else:
            return 2


# does not error handle lmao
def addCity(city, country, latitude, longitude, population, languages):
    query = 'INSERT INTO city(City, Country, latitude, longitude, population) VALUES (%s, %s, %s, %s, %s)'
    response = _cursor.execute(query, (city, country, latitude, longitude, population))

    query = 'INSERT INTO city_language(City, Country, Language) VALUES (%s, %s, %s)'
    for lang in languages:
        response = _cursor.execute(query, (city, country, lang))

    _database.commit()


def getCountries():
    _cursor.execute("SELECT Country FROM country;")
    my_list = tupleListToList(_cursor.fetchall())
    my_list.append("")
    return my_list


def getLanguages():
    _cursor.execute("SELECT Language FROM language;")
    my_list = tupleListToList(_cursor.fetchall())
    my_list.append("Any additional language")
    return my_list


def getLanguagesMgr():
    _cursor.execute("SELECT Language FROM language;")
    return tupleListToList(_cursor.fetchall())


def getCities():
    _cursor.execute("SELECT City FROM city;")
    my_list = tupleListToList(_cursor.fetchall())
    my_list.append("")
    return my_list


def getAddresses():
    _cursor.execute("SELECT Address, City, Country FROM location;")
    my_list = []
    for item in _cursor.fetchall():
        my_list.append(item[0] + ", " + item[1] + ", " + item[2])
    my_list.append("")
    return my_list


def getLocNames():
    _cursor.execute("SELECT Name FROM location;")
    my_list = tupleListToList(_cursor.fetchall())
    my_list.append("")
    return my_list


def getLocTypes():
    _cursor.execute("SELECT Type FROM location_types;")
    return tupleListToList(_cursor.fetchall())


def getEventCategories():
    _cursor.execute("SELECT Category FROM event_categories;")
    return tupleListToList(_cursor.fetchall())


def getReviewableTypes():
    my_list = getCities() + getAddresses() + getEvents()
    my_list.remove("")
    my_list.remove("")
    return my_list


def timedeltaToDateTime(timdel):
    return str((datetime.min + timdel).time())


def getEvents():
    _cursor.execute("SELECT Name, Date, Start_time, Address, City, Country FROM event;")
    my_list = []
    for item in _cursor.fetchall():
        string = item[0] + ", " + item[3] + ", " + item[4] + ", " + item[5] + ", " + str(item[1]) + ", " + timedeltaToDateTime(item[2])
        my_list.append(string)
    my_list.append("")
    return my_list


def tupleListToList(tuplelist):
    my_list = []
    for item in tuplelist:
        my_list.append(item[0])
    return my_list


# returns list in format [reviewed_item, review_date, score, text]
def pastReviews(username):
    reviews = []  # to return

    # city reviews!
    query = 'SELECT * FROM city_review WHERE Username = %s'
    response = _cursor.execute(query, (username,))
    for row in _cursor.fetchall():
        list1 = []
        list1.append(', '.join([row[1], row[2]]))
        for item in row[3:]:
            list1.append(item)
        reviews.append(list1)

    # location reviews
    query = 'SELECT * FROM location_review WHERE Username = %s'
    response = _cursor.execute(query, (username,))
    for row in _cursor.fetchall():
        list1 = []
        list1.append(', '.join([row[1], row[2], row[3]]))
        for item in row[4:]:
            list1.append(item)
        reviews.append(list1)

    # event reviews
    query = 'SELECT * FROM event_review WHERE Username = %s'
    response = _cursor.execute(query, (username,))
    for row in _cursor.fetchall():
        list1 = []
        list1.append(', '.join([row[1], str(row[2]), str(row[3]), row[4], row[5], row[6]]))
        for item in row[7:]:
            list1.append(item)
        reviews.append(list1)

    return reviews


def writeReview(username, reviewableid, review_date, score, review):
    reviewableid = [x.strip() for x in reviewableid.split(',')]
    noFields = len(reviewableid)

    # city reviews
    if noFields == 1:
        query = 'INSERT INTO city_review (Username, City, Country, Date, Score, Description) VALUES (%s, %s, %s, %s, %s, %s);'
        _cursor.execute(query, (str(username), str(reviewableid[0]), str(getCityCountry(reviewableid[0])), str(review_date), str(score), str(review)))

    # location reviews
    elif noFields == 3:
        query = 'INSERT INTO location_review (Username, Address, City, Country, Date, Score, Description) VALUES (%s, %s, %s, %s, %s, %s, %s);'
        _cursor.execute(query, (username, reviewableid[0], reviewableid[1], reviewableid[2], review_date, score, review))

    # event reviews
    elif noFields > 3:
        print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" + reviewableid[0]
        query = 'INSERT INTO event_review (Username, Name, Date, Start_time, Address, City, Country, Review_date, Score, Review) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
        _cursor.execute(query, (username, reviewableid[0], reviewableid[4], reviewableid[5], reviewableid[1], reviewableid[2], reviewableid[3], review_date, score, review))

    _database.commit()
    return True


def updateReview(username, reviewableid, review_date, score, review):
    reviewableid = [x.strip() for x in reviewableid.split(',')]
    noFields = len(reviewableid)

    # city reviews
    if noFields == 1:
        query = 'UPDATE city_review SET Score = %s, Description = %s WHERE Username = %s AND City = %s AND Country = %s AND Date = %s;'
        _cursor.execute(query, (score, review, username, reviewableid[0], getCityCountry(reviewableid[0]), review_date))

    # location reviews
    elif noFields == 3:
        query = 'INSERT INTO location_review (Username, Address, City, Country, Date, Score, Description) VALUES (%s, %s, %s, %s, %s, %s, %s);'
        _cursor.execute(query, (username, reviewableid[0], reviewableid[1], reviewableid[2], review_date, score, review))

    # event reviews
    elif noFields > 3:
        print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" + reviewableid[0]
        query = 'INSERT INTO event_review (Username, Name, Date, Start_time, Address, City, Country, Review_date, Score, Review) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'
        _cursor.execute(query, (username, reviewableid[0], reviewableid[4], reviewableid[5], reviewableid[1], reviewableid[2], reviewableid[3], review_date, score, review))

    #_database.commit()
    return True

setupConnection()
updateReview('nancy', 'Monaco', '2016-07-19', 4, 'Amazing city!!')

query = "SELECT * FROM city_review WHERE Username = %s"
_cursor.execute(query, ('nancy',))
print _cursor.fetchall()
closeConnection()


def aboutCountry(country):
    query = "SELECT * FROM country WHERE Country = %s;"
    response = _cursor.execute(query, (country,))
    fetch = _cursor.fetchone()

    result = {}
    result['name'] = fetch[0]
    result['population'] = fetch[1]
    result['capitals'] = getCapitals(country)
    result['languages'] = getLanguagesCountry(country)

    return result


def aboutCity(city):
    query = 'SELECT * FROM city WHERE City = %s;'
    response = _cursor.execute(query, (city,))

    item = _cursor.fetchone()
    result = {}
    result['name'] = item[0]
    result['country'] = item[1]
    result['gps'] = item[2] + ", " + item[3]
    result['population'] = item[4]
    result['languages'] = getLanguagesCity(city)
    result['score'] = getCityScore(city)
    return result


def aboutLocation(address):
    addressarr = [x.strip() for x in address.split(',')]
    query = "SELECT * FROM location WHERE Address = %s AND City = %s;"
    response = _cursor.execute(query, (addressarr[0], addressarr[1]))

    dicti = {}
    item = _cursor.fetchone()
    dicti['name'] = item[6]
    dicti['address'] = item[0] + ", " + item[1] + ", " + item[2]
    dicti['cost'] = item[3]
    dicti['std_discount'] = item[5]
    dicti['category'] = item[4]
    dicti['score'] = getLocScore(item[0], item[1], item[2])

    return dicti


def aboutEvent(key):
    eventarr = [x.strip() for x in key.split(',')]
    query = "SELECT * FROM Event WHERE Name = %s AND Address = %s AND City = %s"
    query += " AND Country = %s AND Date = %s AND Start_time = %s;"

    response = _cursor.execute(query, tuple(eventarr))
    item = _cursor.fetchone()
    dicti = {}
    dicti['name'] = item[0]
    dicti['date'] = str(item[1])
    dicti['starttime'] = str(item[2])
    dicti['location'] = item[3] + ", " + item[4] + ", " + item[5]
    dicti['endtime'] = str(item[9])
    dicti['cost'] = item[10]
    dicti['std_discount'] = "Yes" if item[8] else "No"
    dicti['category'] = item[6]
    dicti['score'] = getEventScore(item[0], item[1], item[2], item[3], item[4])

    return dicti


def getEventReviews(key):
    eventarr = [x.strip() for x in key.split(',')]
    query = "SELECT * FROM event_review WHERE Name = %s AND Address = %s AND City = %s"
    query += " AND Country = %s AND Date = %s AND Start_time = %s;"
    response = _cursor.execute(query, eventarr)

    result = []
    for item in _cursor.fetchall():
        dicti = {}
        dicti['username'] = item[0]
        dicti['date'] = item[7]
        dicti['score'] = item[8]
        dicti['description'] = item[9]
        result.append(dicti)
    return result


def getLocationEvents(address):
    addressarr = [x.strip() for x in address.split(',')]
    query = "SELECT * FROM event WHERE Address = %s AND City = %s;"
    response = _cursor.execute(query, (addressarr[0], addressarr[1]))

    result = []
    for item in _cursor.fetchall():
        dicti = {}
        dicti['event'] = item[0]
        dicti['date'] = item[1]
        dicti['time'] = item[2]
        dicti['category'] = item[6]
        dicti['score'] = getEventScore(item[0], item[1], item[2], item[3], item[4])
        result.append(dicti)
    return result


def getLocationReviews(address):
    addressarr = [x.strip() for x in address.split(',')]
    query = "SELECT * FROM location_review WHERE Address = %s AND City = %s;"
    response = _cursor.execute(query, (addressarr[0], addressarr[1]))

    result = []
    for item in _cursor.fetchall():
        dicti = {}
        dicti['username'] = item[0]
        dicti['date'] = item[4]
        dicti['score'] = item[5]
        dicti['description'] = item[6]
        result.append(dicti)
    return result


def getCityLocations(city):
    query = "SELECT * FROM location WHERE city = %s;"
    response = _cursor.execute(query, (city,))

    result = []
    for item in _cursor.fetchall():
        dicti = {}
        dicti['name'] = item[6]
        dicti['type'] = item[4]
        dicti['cost'] = item[3]
        dicti['score'] = getLocScore(item[0], item[1], item[2])
        result.append(dicti)
    return result


def getCityReviews(city):
    query = "SELECT * FROM city_review NATURAL JOIN city WHERE City = %s;"
    response = _cursor.execute(query, (city,))

    result = []
    for item in _cursor.fetchall():
        dicti = {}
        dicti['username'] = item[2]
        dicti['date'] = item[3]
        dicti['score'] = item[4]
        dicti['description'] = item[5]
        result.append(dicti)
    return result


def getCountryCities(country):
    query = "SELECT City, Population FROM city WHERE Country = %s;"
    response = _cursor.execute(query, (country,))

    result = []
    for item in _cursor.fetchall():
        dicti = {}
        dicti['city'] = item[0]
        dicti['population'] = item[1]
        dicti['languages'] = getLanguagesCity(item[0])
        dicti['score'] = getCityScore(item[0])
        result.append(dicti)
    return result


def countrySearch(country, population_min, population_max, lang_list, sort):
    population = population_max or population_min
    cri = False
    if lang_list and "Any additional language" in lang_list:
        cri = True
        lang_list.remove('Any additional language')

    if country:
        query = "SELECT * FROM country WHERE Country = %s;"
        response = _cursor.execute(query, (country,))
        fetch = _cursor.fetchone()
        result = {}
        result['name'] = fetch[0]
        result['population'] = fetch[1]

        result['capitals'] = getCapitals(country)
        result['languages'] = getLanguagesCountry(country)

        return [result]
    elif population and lang_list:
        languages = '\' OR Language = \''.join(lang_list)
        langquery = 'Language = \'' + languages + '\''
        innerquery = "(SELECT * FROM country_language WHERE " + langquery + ") q "

        query = "SELECT * FROM " + innerquery + "NATURAL JOIN country"
        if cri:
            query += ") p"
            query = "SELECT * FROM multlangcountries NATURAL JOIN (" + query
        query += " WHERE "

        if population_min and population_max:
            query += "Population >= %s AND Population <= %s ORDER BY Population DESC"
            response = _cursor.execute(query, (population_min, population_max))
        elif population_max:
            query = query + "Population <= %s ORDER BY Population DESC"
            response = _cursor.execute(query, (population_max,))
        elif population_min:
            query = query + "Population >= %s ORDER BY Population DESC"
            response = _cursor.execute(query, (population_min,))
        else:
            print "shouldn't get here"  # sanity check

        result = []
        for item in _cursor.fetchall():
            put = {}
            put['name'] = item[0]
            put['population'] = item[2]
            put['capitals'] = getCapitals(item[0])
            put['languages'] = getLanguagesCountry(item[0])
            result.append(put)

        if cri:
            return [dict(t) for t in set([tuple(d.items()) for d in result])]
        else:
            return result
    elif population:
        query = "SELECT Country, Population FROM country WHERE "

        response = ""

        if population_min and population_max:
            query = query + "Population >= %s AND Population <= %s ORDER BY Population DESC;"
            response = _cursor.execute(query, (population_min, population_max))
        elif population_max:
            query = query + "Population <= %s ORDER BY Population DESC;"
            response = _cursor.execute(query, (population_max,))
        elif population_min:
            query = query + "Population >= %s ORDER BY Population DESC;"
            response = _cursor.execute(query, (population_min,))

        result = []
        for item in _cursor.fetchall():
            put = {}
            put['name'] = item[0]
            put['population'] = item[1]
            put['capitals'] = getCapitals(item[0])
            put['languages'] = getLanguagesCountry(item[0])
            result.append(put)

        return result
    elif lang_list:
        languages = '\' OR Language = \''.join(lang_list)
        langquery = 'Language = \'' + languages + '\''
        if cri:
            query = "SELECT * FROM multlangcountries NATURAL JOIN "\
            "(SELECT * FROM (SELECT Country FROM country_language WHERE "
            query += langquery + ") q NATURAL JOIN country) p;"
        else:
            query = "SELECT * FROM (SELECT Country FROM country_language WHERE "
            query += langquery + ") q NATURAL JOIN country;"
        response = _cursor.execute(query)

        result = []
        for item in _cursor.fetchall():
            put = {}
            print item
            put['name'] = item[0]
            put['population'] = item[1]
            put['capitals'] = getCapitals(item[0])
            put['languages'] = getLanguagesCountry(item[0])
            result.append(put)

        if cri:
            return [dict(t) for t in set([tuple(d.items()) for d in result])]
        else:
            return result
    else:
        query = "SELECT * FROM country;"
        response = _cursor.execute(query)

        result = []
        for item in _cursor.fetchall():
            put = {}
            put['name'] = item[0]
            put['population'] = item[1]
            put['capitals'] = getCapitals(item[0])
            put['languages'] = getLanguagesCountry(item[0])
            result.append(put)

        return result


# returns a country's capitals in a string
def getCapitals(country):
    query = "SELECT Capital FROM capitals WHERE Country = %s;"
    response = _cursor.execute(query, (country,))
    capitals = []
    for row in _cursor.fetchall():
        capitals.append(row[0])
    capitals = ', '.join(capitals)
    return capitals


# returns a country's languages in a string
def getLanguagesCountry(country):
    query = "SELECT Language FROM country_language WHERE Country = %s;"
    response = _cursor.execute(query, (country,))
    languages = []
    for row in _cursor.fetchall():
        languages.append(row[0])
    languages = ', '.join(languages)
    return languages


# returns a city's languages in a string
def getLanguagesCity(city):
    query = "SELECT Language FROM city_language WHERE City = %s;"
    response = _cursor.execute(query, (city,))
    languages = []
    for row in _cursor.fetchall():
        languages.append(row[0])
    languages = ', '.join(languages)
    return languages


def isCapital(city):
    query = "SELECT * FROM capitals WHERE Capital = %s;"
    response = _cursor.execute(query, (city,))
    return response > 0


def getCityScore(city):
    query = "SELECT Average_score FROM city_scores WHERE City = %s;"
    response = _cursor.execute(query, (city,))
    fetch = _cursor.fetchone()
    return fetch[0] if fetch else "N/A"


# returns specific city in format [city, country, latitude, longitude,
#       population, is_capital, [languages]]
# returns
def citySearch(city, country, population_min, population_max, lang_list, sort):
    population = population_max or population_min

    if city:  # searching by city, returns just info about that city
        dicti = {}
        query = "SELECT * FROM city WHERE City = %s;"
        response = _cursor.execute(query, (city,))
        result = _cursor.fetchone()
        dicti['city'] = result[0]
        dicti['country'] = result[1]
        dicti['latitude'] = result[2]
        dicti['longitude'] = result[3]
        dicti['population'] = result[4]
        dicti['iscapital'] = isCapital(city)
        dicti['languages'] = getLanguagesCity(city)
        dicti['score'] = getCityScore(city)

        return [dicti]
    elif country and population and lang_list:
        print 1
    elif country and population:
        print 2
    elif country and lang_list:
        print 3
    elif population and lang_list:
        print 4
    elif country:
        print 5
    elif population:
        print 6
    elif lang_list:
        print 7
    else:
        query = "SELECT * FROM city;"
        response = _cursor.execute(query)

        result = []
        for item in _cursor.fetchall():
            dicti = {}
            dicti['city'] = item[0]
            dicti['country'] = item[1]
            dicti['latitude'] = item[2]
            dicti['longitude'] = item[3]
            dicti['population'] = item[4]
            dicti['iscapital'] = isCapital(item[0])
            dicti['languages'] = getLanguagesCity(item[0])
            dicti['score'] = getCityScore(item[0])
            result.append(dicti)
        return result


def locationSearch(name, address, city, cost_min, cost_max, type_list, sort):
    '''cost = cost_min or cost_max
    #std_discount = "TRUE" if std_discount == True else "FALSE"

    if address:
        addressarr = [x.strip() for x in address.split(',')]
        query = "SELECT * FROM location WHERE Address = %s AND City = %s AND Country = %s"
        response = _cursor.execute(query, tuple(addressarr))

        return getLocInfo(_cursor.fetchall())
    elif name and city and cost and type_list:
        print 1
    # elif name and country and cost and type_list:
    #     print 2
    elif name and city and cost:
        print 3
    elif name and city and type_list:
        print 3
    # elif name and country and cost:
    #     print 3
    # elif name and country and type_list:
    #     print 4
    elif name and cost and type_list:
        print 3
    elif city and cost and type_list:
        print 3
    # elif country and cost and type_list:
    #     print 3
    elif name and city:
        print 3
    # elif name and country:
    #     print 3
    elif name and cost:
        print 3
    elif name and type_list:
        print 3
    elif city and cost:
        print 3
    elif city and type_list:
        print 3
    # elif country and cost:
    #     print 3
    # elif country and type_list:
    #     print 3
    elif cost and type_list:
        print 3
    elif name:
        print 2
    elif city:
        print 3
    # elif country:
    #     print 2
    elif cost:
        print 3
    elif type_list:
        print 3
    else:
        query = "SELECT * FROM location;"
        response = _cursor.execute(query)

        return getLocInfo(_cursor.fetchall()) */'''

    query = 'SELECT * FROM location l'

    if sort:
        if sort == 'highest':
            query = 'SELECT l.Address, l.City, l.Country, l.Cost, l.Type, l.Std_discount, l.Name, AVG(lr.Score) FROM location l NATURAL JOIN location_review lr'
            ps = ' GROUP BY l.Address, l.City, l.Country ORDER BY 8 DESC' # AVG Score and GROUP BY prevent duplicates
        if sort == 'location':
            ps = ' ORDER BY l.Name ASC'
        if sort == 'lowest':
            query = 'SELECT l.Address, l.City, l.Country, l.Cost, l.Type, l.Std_discount, l.Name, AVG(lr.Score) FROM location l NATURAL JOIN location_review lr'
            ps = ' GROUP BY l.Address, l.City, l.Country ORDER BY 8 ASC'
        if sort == 'type':
            ps = ' ORDER BY l.Type ASC'
    else:
        ps = ''

    if name or address or city or cost_min or cost_max:
        query = query + " WHERE"
    if name:
        query = query + " l.Name = '" + str(name) + "' AND "
    if address:         # TODO: why does address take precedence in searching
        query = query + " l.Address = '" + str(address) + "' AND "
    if city:
        query = query + " l.City = '" + str(city) + "' AND "
    if cost_min:
        query = query + " l.Cost > '" + str(cost_min) + "' AND "
    if cost_max:
        query = query + " l.Cost < '" + str(cost_max) + "' AND "
        query = query + " Cost >= '" + str(cost_min) + "' AND "
    if cost_max:
        query = query + " Cost <= '" + str(cost_max) + "' AND "

    print type_list
    if type_list:
        pass                 # TODO: type_list empty

    if query[-5:] == ' AND ':
        query = query[:-5]

    query = query + ps

    _cursor.execute(query)
    response = _cursor.fetchall()
    # return response
    return getLocInfo(response)


def getTypeQuery(type_list):
    query = '\' OR Type = \''.join(type_list)
    query = '(Type = \'' + query + '\')'
    return query


def getLocInfo(tuplelist):
    result = []
    for item in tuplelist:
        dicti = {}
        dicti['name'] = item[6]
        dicti['address'] = item[0]
        dicti['city'] = item[1]
        dicti['country'] = item[2]
        dicti['cost'] = item[3]
        dicti['type'] = item[4]
        dicti['std_discount'] = 'No' if item[5] else 'Yes'
        dicti['score'] = getLocScore(item[0], item[1], item[2])
        result.append(dicti)
    return result


def getLocScore(address, city, country):
    query = "SELECT Average_score FROM location_scores WHERE Address = %s "\
            "AND City = %s AND Country = %s;"
    response = _cursor.execute(query, (address, city, country))
    fetch = _cursor.fetchone()
    return fetch[0] if fetch else "N/A"


def getCatQuery(cat_list):
    query = '\' OR Category = \''.join(cat_list)
    query = '(Category = \'' + query + '\')'
    return query


# param std_discount is None if not selected, True if yes, and False if no
def eventSearch(event, city, date, cost_min, cost_max, std_discount, cat_list, sort):
    cost = cost_max or cost_min
    std_discount = "TRUE" if std_discount == True else "FALSE"

    if event:
        eventarr = [x.strip() for x in event.split(',')]
        query = "SELECT * FROM Event WHERE Name = %s AND Address = %s AND City = %s"
        query += " AND Country = %s AND Date = %s AND Start_time = %s;"
        response = _cursor.execute(query, tuple(eventarr))

        return getEventInfo(_cursor.fetchall())
    elif city and date and cost and std_discount and cat_list:
        query = "SELECT * FROM EVENT WHERE city = %s AND  date = %s "
        query += "AND std_discount = " + std_discount + " AND " + getCatQuery(cat_list)
        if cost_max and cost_min:
            query += " AND Cost >= %s AND Cost <= %s "
            response = _cursor.execute(query, (city, date, cost_min, cost_max))
        elif cost_max:
            query += " AND Cost <= %s "
            response = _cursor.execute(query, (city, date, cost_max))
        else:  # elif cost_min
            query += " AND Cost >= %s "
            response = _cursor.execute(query, (city, date, cost_min))

        return getEventInfo(_cursor.fetchall())
    elif date and cost and std_discount and cat_list:
        query = "SELECT * FROM EVENT WHERE date = %s AND  cost = %s AND  std_discount = TRUE AND  %s IN cat_list;"

        return getEventInfo(_cursor.fetchall())
    elif city and cost and std_discount and cat_list:
        query = "SELECT * FROM EVENT WHERE city = %s "
        query += "AND std_discount = " + std_discount + " AND " + getCatQuery(cat_list)

        if cost_max and cost_min:
            query += " AND Cost >= %s AND Cost <= %s "
            response = _cursor.execute(query, (city, cost_min, cost_max))
        elif cost_max:
            query += " AND Cost <= %s "
            response = _cursor.execute(query, (city, cost_max))
        else:  # elif cost_min
            query += " AND Cost >= %s "
            response = _cursor.execute(query, (city, cost_min))

        return getEventInfo(_cursor.fetchall())
    elif city and date and std_discount and cat_list:
        query = "SELECT * FROM EVENT WHERE city = %s AND  date = %s AND  std_discount = TRUE AND  %s IN cat_list;"

        return getEventInfo(_cursor.fetchall())
    elif city and date and cost and cat_list:
        query = "SELECT * FROM EVENT WHERE city = %s AND  date = %s AND  cost = %s AND  %s IN cat_list;"

        return getEventInfo(_cursor.fetchall())
    elif city and date and cost and std_discount:
        query = "SELECT * FROM EVENT WHERE city = %s AND  date = %s AND  cost = %s AND  std_discount = TRUE;"

        if cost_max and cost_min:
            query += " AND Cost >= %s AND Cost <= %s "
            response = _cursor.execute(query, (city, cost_min, cost_max))
        elif cost_max:
            query += " AND Cost <= %s "
            response = _cursor.execute(query, (city, cost_max))
        else:  # elif cost_min
            query += " AND Cost >= %s "
            response = _cursor.execute(query, (city, cost_min))

        return getEventInfo(_cursor.fetchall())
    elif city and date and cost:
        query = "SELECT * FROM EVENT WHERE city = %s AND  date = %s AND  cost = %s;"

        if cost_max and cost_min:
            query += " AND Cost >= %s AND Cost <= %s "
            response = _cursor.execute(query, (city, cost_min, cost_max))
        elif cost_max:
            query += " AND Cost <= %s "
            response = _cursor.execute(query, (city, cost_max))
        else:  # elif cost_min
            query += " AND Cost >= %s "
            response = _cursor.execute(query, (city, cost_min))

        return getEventInfo(_cursor.fetchall())
    elif city and date and std_discount:
        query = "SELECT * FROM EVENT WHERE city = %s AND  date = %s AND  std_discount = TRUE;"

        return getEventInfo(_cursor.fetchall())
    elif city and date and cat_list:
        query = "SELECT * FROM EVENT WHERE city = %s AND  date = %s AND  %s IN cat_list;"

        return getEventInfo(_cursor.fetchall())
    elif city and cost and std_discount:
        query = "SELECT * FROM EVENT WHERE city = %s AND  cost = %s AND  std_discount = TRUE;"

        if cost_max and cost_min:
            query += " AND Cost >= %s AND Cost <= %s "
            response = _cursor.execute(query, (city, cost_min, cost_max))
        elif cost_max:
            query += " AND Cost <= %s "
            response = _cursor.execute(query, (city, cost_max))
        else:  # elif cost_min
            query += " AND Cost >= %s "
            response = _cursor.execute(query, (city, cost_min))

        return getEventInfo(_cursor.fetchall())
    elif city and cost and cat_list:
        query = "SELECT * FROM EVENT WHERE city = %s AND  cost = %s AND  %s IN cat_list;"

        if cost_max and cost_min:
            query += " AND Cost >= %s AND Cost <= %s "
            response = _cursor.execute(query, (city, cost_min, cost_max))
        elif cost_max:
            query += " AND Cost <= %s "
            response = _cursor.execute(query, (city, cost_max))
        else:  # elif cost_min
            query += " AND Cost >= %s "
            response = _cursor.execute(query, (city, cost_min))

        return getEventInfo(_cursor.fetchall())
    elif city and std_discount and cat_list:
        query = "SELECT * FROM EVENT WHERE city = %s AND  std_discount = TRUE AND  %s IN cat_list;"

        return getEventInfo(_cursor.fetchall())
    elif date and cost and std_discount:
        query = "SELECT * FROM EVENT WHERE date = %s AND  cost = %s AND  std_discount = TRUE;"

        if cost_max and cost_min:
            query += " AND Cost >= %s AND Cost <= %s "
            response = _cursor.execute(query, (city, cost_min, cost_max))
        elif cost_max:
            query += " AND Cost <= %s "
            response = _cursor.execute(query, (city, cost_max))
        else:  # elif cost_min
            query += " AND Cost >= %s "
            response = _cursor.execute(query, (city, cost_min))

        return getEventInfo(_cursor.fetchall())
    elif date and cost and cat_list:
        query = "SELECT * FROM EVENT WHERE date = %s AND  cost = %s AND  %s IN cat_list;"

        if cost_max and cost_min:
            query += " AND Cost >= %s AND Cost <= %s "
            response = _cursor.execute(query, (city, cost_min, cost_max))
        elif cost_max:
            query += " AND Cost <= %s "
            response = _cursor.execute(query, (city, cost_max))
        else:  # elif cost_min
            query += " AND Cost >= %s "
            response = _cursor.execute(query, (city, cost_min))

        return getEventInfo(_cursor.fetchall())
    elif date and std_discount and cat_list:
        query = "SELECT * FROM EVENT WHERE date = %s AND  std_discount = TRUE AND  %s IN cat_list;"

        return getEventInfo(_cursor.fetchall())
    elif cost and std_discount and cat_list:
        query = "SELECT * FROM EVENT WHERE cost = %s AND  std_discount = TRUE AND  %s IN cat_list;"

        if cost_max and cost_min:
            query += " AND Cost >= %s AND Cost <= %s "
            response = _cursor.execute(query, (city, cost_min, cost_max))
        elif cost_max:
            query += " AND Cost <= %s "
            response = _cursor.execute(query, (city, cost_max))
        else:  # elif cost_min
            query += " AND Cost >= %s "
            response = _cursor.execute(query, (city, cost_min))

        return getEventInfo(_cursor.fetchall())
    elif city and date:
        query = "SELECT * FROM EVENT WHERE city = %s AND  date = %s;"

        return getEventInfo(_cursor.fetchall())
    elif city and cost:
        query = "SELECT * FROM EVENT WHERE city = %s AND  cost = %s;"

        if cost_max and cost_min:
            query += " AND Cost >= %s AND Cost <= %s "
            response = _cursor.execute(query, (city, cost_min, cost_max))
        elif cost_max:
            query += " AND Cost <= %s "
            response = _cursor.execute(query, (city, cost_max))
        else:  # elif cost_min
            query += " AND Cost >= %s "
            response = _cursor.execute(query, (city, cost_min))

        return getEventInfo(_cursor.fetchall())
    elif city and std_discount:
        query = "SELECT * FROM EVENT WHERE city = %s AND  std_discount = TRUE;"

        return getEventInfo(_cursor.fetchall())
    elif city and cat_list:
        query = "SELECT * FROM EVENT WHERE city = %s AND  %s IN cat_list;"

        return getEventInfo(_cursor.fetchall())
    elif date and cost:
        query = "SELECT * FROM EVENT WHERE date = %s AND  cost = %s;"

        if cost_max and cost_min:
            query += " AND Cost >= %s AND Cost <= %s "
            response = _cursor.execute(query, (city, cost_min, cost_max))
        elif cost_max:
            query += " AND Cost <= %s "
            response = _cursor.execute(query, (city, cost_max))
        else:  # elif cost_min
            query += " AND Cost >= %s "
            response = _cursor.execute(query, (city, cost_min))

        return getEventInfo(_cursor.fetchall())
    elif date and std_discount:
        query = "SELECT * FROM EVENT WHERE date = %s AND  std_discount = TRUE;"

        return getEventInfo(_cursor.fetchall())
    elif date and cat_list:
        query = "SELECT * FROM EVENT WHERE date = %s AND  %s IN cat_list;"

        return getEventInfo(_cursor.fetchall())
    elif cost and std_discount:
        query = "SELECT * FROM EVENT WHERE cost = %s AND  std_discount = TRUE;"

        if cost_max and cost_min:
            query += " AND Cost >= %s AND Cost <= %s "
            response = _cursor.execute(query, (city, cost_min, cost_max))
        elif cost_max:
            query += " AND Cost <= %s "
            response = _cursor.execute(query, (city, cost_max))
        else:  # elif cost_min
            query += " AND Cost >= %s "
            response = _cursor.execute(query, (city, cost_min))

        return getEventInfo(_cursor.fetchall())
    elif cost and cat_list:
        query = "SELECT * FROM EVENT WHERE cost = %s AND  %s IN cat_list;"

        if cost_max and cost_min:
            query += " AND Cost >= %s AND Cost <= %s "
            response = _cursor.execute(query, (city, cost_min, cost_max))
        elif cost_max:
            query += " AND Cost <= %s "
            response = _cursor.execute(query, (city, cost_max))
        else:  # elif cost_min
            query += " AND Cost >= %s "
            response = _cursor.execute(query, (city, cost_min))

        return getEventInfo(_cursor.fetchall())
    elif std_discount and cat_list:
        query = "SELECT * FROM EVENT WHERE std_discount = TRUE AND  %s IN cat_list;"

        return getEventInfo(_cursor.fetchall())
    elif city:
        query = "SELECT * FROM Event WHERE City = %s;"
        response = _cursor.execute(query, (city,))

        return getEventInfo(_cursor.fetchall())
    elif date:
        query = "SELECT * FROM Event WHERE Date = %s;"
        response = _cursor.execute(query, (date,))


        return getEventInfo(_cursor.fetchall())

    elif cost:
        query = "SELECT * FROM EVENT WHERE cost = %s;"

        return getEventInfo(_cursor.fetchall())
    elif std_discount:
        query = "SELECT * FROM EVENT WHERE std_discount = TRUE;"

        return getEventInfo(_cursor.fetchall())
    elif cat_list:
        query = "SELECT * FROM EVENT WHERE %s IN cat_list;"

        return getEventInfo(_cursor.fetchall())
    else:
        print "shouldn't be here - event search"  # sanity check


def getEventInfo(tuplelist):
    list1 = []
    for item in tuplelist:
        dicti = {}
        dicti['name'] = item[0]
        dicti['date'] = str(item[1])
        dicti['starttime'] = str(item[2])
        dicti['address'] = item[3]
        dicti['city'] = item[4]
        dicti['country'] = item[5]
        dicti['category'] = item[6]
        dicti['description'] = item[7]
        dicti['std_discount'] = 'Yes' if item[8] else 'No'
        dicti['endtime'] = 'unknown' if item[9] == None else str(item[9])
        dicti['cost'] = item[10]
        dicti['score'] = getEventScore(item[0], item[1], item[2], item[3], item[4])
        list1.append(dicti)
    return list1


# doesn't work, lmao
def getEventScore(name, date, starttime, address, city):
    query = "SELECT Average_score FROM event_scores WHERE Name = %s AND Date = %s"\
            " AND Start_time = %s AND Address = %s AND City = %s;"
    response = _cursor.execute(query, (name, date, starttime, address, city))
    fetch = _cursor.fetchone()
    return fetch[0] if fetch else "N/A"

# helper for writeReviews
def getCityCountry(city):
    query = "SELECT Country FROM city WHERE City = %s"
    response = _cursor.execute(query, (city,))
    fetch = _cursor.fetchone()
    # country = fetch[0].strip()
    # country = str(country)
    return fetch[0] if fetch else "N/A"

## testing
setupConnection()

#print writeReview()
# code for SELECT for testing :)
# _cursor.execute("SELECT * FROM city_language")
# for row in _cursor.fetchall():
#     print row

# print citySearch(None, None, None, None, None)

closeConnection()
