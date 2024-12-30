from typing import Dict

from fastapi import FastAPI
from constants import *
import re
from tinydb import TinyDB, Query


app = FastAPI()

def vDate(text):
    regex = re.compile(DATE_REGEX)
    find = re.findall(regex, text)
    if len(find)>0:
        return True
    else:
        return False

def vPhone(text):
    regex = re.compile(PHONE_REGEX)
    find = re.findall(regex, text)
    if len(find)>0:
        return True
    else:
        return False


def vEmail(text):
    regex = re.compile(EMAIL_REGEX)
    find = re.findall(regex, text)
    if len(find)>0:
        return True
    else:
        return False

def vText(text):
    if isinstance(text, str):
        return True
    else:
        return False


def compareTypes(ct1, ct2, compareFunc):
    if (compareFunc(ct1) & compareFunc(ct2)):
        return True
    else:
        return False


def validate(forms, fields)-> list:
    validated = []

    for form in forms:
        vRes = []
        for key in fields:
            tFunctions = [vEmail, vText, vPhone, vDate]
            for tF in tFunctions:
                vRes += [compareTypes(form[key], fields[key], tF)]
        if any(vRes):
            validated += [True]
        else:
            validated += [False]
    return validated


def printTypes(fields):
    ret = {}
    for key in fields:
        if (not isinstance(fields[key],str)):
            ret[key] = "UNKNOWN"
        elif (vEmail(fields[key])):
            ret[key] = "EMAIL"
        elif (vDate(fields[key])):
            ret[key] = "DATE"
        elif (vPhone(fields[key])):
            ret[key] = "PHONE"
        else:
            ret[key] = "TEXT"
    return ret


@app.post("/get_form")
async def getForm(fields: Dict):
    db = TinyDB(PATH_TO_DB)
    print(fields)
    ret = []
    qForm = Query()
    fNames = list(fields.keys())
    req = qForm[fNames[0]].exists()
    for f in range(1, len(fNames)):
        req = req & qForm[fNames[f]].exists()
    forms = db.search(req)
    if (len(forms) > 0):
        validated = validate(forms, fields)
        for f in range(len(validated)):
            if validated[f] == True:
                ret += [forms[f]["name"]]
            else:
                ret += [forms[f]["name"]]
    else:
        ret = printTypes(fields)
    return ret