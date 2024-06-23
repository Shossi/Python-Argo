from googletrans import Translator  # used in translate_country to translate the text to english


def translate_country(data):
    """
    Function that translates country name to english.
    uses googletrans library to do so. and returns the country in english.
    :param data: data from the api, in form of json
    :return: returns translated country.
    """
    translator = Translator()
    country = translator.translate(data['resolvedAddress']).text
    return country
