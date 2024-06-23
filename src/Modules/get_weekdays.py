from datetime import datetime  # used in the get_weekdays function to parse str to day names


def get_weekdays(data):
    """
    function that recieves the data from the apicall and creates a list
    containing the following week days, starting from today.
    :param data: data from the api, in form of json
    :return: list of the following week days.
    """
    days_list = []
    for i in range(7):
        day = datetime.strptime(data['days'][i]['datetime'], '%Y-%m-%d')
        day = day.strftime('%A')
        days_list.append(day)
    return days_list
