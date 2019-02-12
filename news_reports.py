## Generate a set of analytical reports for the
# News data database.

import datetime
import psycopg2

##
# Defined constants
#
DBNAME = "news"

##
# runQuery takes a postgresql query string and optional set
# of query parameters and attempts to execute the query.
#
# @param {String} query : the query string to be executed.
# @param {tuple} query_params : query params to be inserted into
# the query.
#
# @return {list} if the query resulted in returned records,
# those records will be returned as a list of tuples.
#
# @return {void} if an error occured during the query, the
# function simply returns.
##
def runQuery(query, query_params=None):

    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()

    try:
        if query_params:
            c.execute(query, query_params)
        else:
            c.execute(query)
    except psycopg2.Error as e:
        print(e.pgerror)
        return

    return c.fetchall()
    db.close()


##
# getMostPopularArticles prints the top articles by number of views.
#
# @param {int} numArticles : the number of articles to be returned.
#
##
def getMostPopularArticles(numArticles):

    doSectionHeader("Top articles by number of views")

    displayTemplate = "## \"{0}\"--{1:d}"
    q = """
        select title, count(*) as views
        from articles join log
            on log.path = '/article/'||articles.slug
        group by articles.title
        order by views desc
        limit (%s);
    """

    articles = runQuery(q, (3,))

    if len(articles) > 0:
        for a in articles:
            print(displayTemplate.format(*a))
    else:
        print("No artciles found.")

    doSectionFooter()


##
# getMostPopularAuthors prints a list of authors ordered by the
# number of views their articles have received.
#
##
def getMostPopularAuthors():

    doSectionHeader("Author popularity by views")

    displayTemplate = "## {0}--{1:d} views"
    q = """
        select name, count(*) as views
        from authors
            join articles on articles.author = authors.id
            join log on log.path = '/article/' ||articles.slug
        group by authors.name
        order by views desc;
    """

    authors = runQuery(q)

    if len(authors) > 0:
        for auth in authors:
            print(displayTemplate.format(*auth))
    else:
        print("No Authors Found")

    doSectionFooter()


##
# getHighErrorDays prints a list of any days where the percentage
# of log entries showing anothing other than a 200 response compared
# to the total number of log entries for that day, is greater than 1%.
#
# This function requires the log_stats view.  Specifics on the
# view can be found in the README.md
#
##
def getHighErrorDays():

    doSectionHeader("Days with error responses over 1 %")

    displayTemplate = "## {0}--{1:.1f}% errors"
    q = """
        select * from log_stats
        where error_percentage >= 1;
    """

    days = runQuery(q)

    if len(days) > 0:
        for d in days:
            print(displayTemplate.format(d[0].strftime("%B, %d %Y"),d[3]))

    doSectionFooter()


##
# doSectionHeader simply prints a section header.
#
# @param {string} title : the title to be included in
# the header
##
def doSectionHeader(title):
    print("## {:s}".format(title))
    print("## -----------------------------------")


##
# doSectionFooter prints a simple section footer.
#
##
def doSectionFooter():
    print("##\n## -----------------------------------\n##")


##
# Runs the program.
#
##
def run():
    getMostPopularArticles(3)
    getMostPopularAuthors()
    getHighErrorDays()


run()
