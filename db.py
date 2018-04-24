from flask import request

def create_record(_class, _request, _record):
    # _record is empty, only Ids
    try:
        for _field in _class.keys():
            if _field not in _record.keys():
                _record[_field] = request.json.get(_field, _class[_field]())
    except:
        return False
    return True

def update_record(_class, _request, _record):
    for _field in _class.keys():
        if _field in request.json:
            _record[_field] = request.json[_field]

def check_record(_class, _request, _record):
    for _field in _class.keys():
        if _field in request.json:
            if _class[_field] != type(request.json[_field]):
                return False
    return True
