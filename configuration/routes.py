from flask import Blueprint, jsonify 
from configuration.utils import getCountries, getLanguages, getTimezones
import configuration

configuration = Blueprint('configuration', __name__)

@configuration.route('/api/configuration/countries')
def getCountriesMain():
    countriesList = getCountries()
    return jsonify(countriesList)

@configuration.route('/api/configuration/languages')
def getLanguagesMain():
    languageList = getLanguages()
    return jsonify(languageList)

@configuration.route('/api/configuration/timezones')
def getTimezonesMain():
    timezonesList = getTimezones()
    return jsonify(timezonesList)
