from flask import Blueprint, jsonify, request
from api import db
from api.models import word_search
from sqlalchemy.sql.expression import func

utils = Blueprint('utils', __name__)

results = {
    'code'      : 0,
    'message'   : "Failure",
}

@utils.route("/search", methods=['GET'])
def words():
    try:
        returndataArr = []
        word = request.args.get('word')
        words = word_search.query.filter(word_search.word.like("%"+word+"%"))\
                    .order_by(func.length(word_search.word),
                    word_search.frequency.desc())\
                    .limit(25).all()
        if len(words)>1:
            returndataArr = [i.serialize for i in words]
            results['code'] = 1
            results['message'] = "success"
            results['count'] = len(words)
            results['data'] = returndataArr

        return jsonify(results=results)
    except:
        return jsonify(results=results)


@utils.route("/")
def home():
    results['code'] = 1
    results['message'] = "success"
    results['data'] = """
        Try searching words.Api url endpoint = '/search?word=pro'"""

    # # try:
    # objects = []
    # with open("word_search.tsv") as f:
    #     for line in f:
    #         lineData = line.split('\t')
    #         word = word_search(word=lineData[0], frequency=lineData[1][:-1])
    #         objects.append(word)
    # db.session.add_all(objects)
    # db.session.commit()
    #
    # results['code'] = 1
    # results['message'] = "success"
    # results['data'] = "success : {}".format(len(objects))
    # # except:
    # #     return False

    return jsonify(results=results)
