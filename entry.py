from microdot import Microdot
from datetime import datetime
from psutil import disk_usage, sensors_temperatures, boot_time

app = Microdot()

API_MSG_ENUM = {
    0: 'success',
    404: 'no data',
    522: 'wrong arguments',
}


def make_json_response(code, data=None):
    """ format the json response """
    if code not in API_MSG_ENUM.keys():
        raise ValueError('illegal code')
    return {
        'code': code,
        'status': API_MSG_ENUM[code],
        'data': data
    }


def readable_time(seconds, granularity=3):
    """
    turn seconds (timedelta) to human-readable format
    from https://stackoverflow.com/questions/4048651/function-to-convert-seconds-into-minutes-hours-and-days
    """
    seconds = int(seconds)
    result = []
    intervals = (
        ('w', 604800),  # weeks 60 * 60 * 24 * 7
        ('d', 86400),  # days 60 * 60 * 24
        ('h', 3600),  # hours 60 * 60
        ('m', 60),  # minutes
        ('s', 1),  # seconds
    )

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            result.append("{}{}".format(value, name))
    return ' '.join(result[:granularity])


@app.route('/stats/<string:data_type>')
def stats(request, data_type):
    """ gather os/hw stats as needed """

    def get_du():
        du = disk_usage('/')
        return {
            'free_size': round(du.free/(2**20), 2),
            'free_rate': round(100 - float(du.percent), 2)
        }

    def get_multiple_temperatures():
        temps = sensors_temperatures()
        return {
            k: {'curr': round(v[0].current, 2) if v[0].current else None,
                'crit': round(v[0].critical, 2) if v[0].critical else None}
            for k, v in temps.items() if v}

    def get_boot_time():
        time_of_boot = datetime.fromtimestamp(boot_time())
        elapsed_seconds = (datetime.now() - time_of_boot).total_seconds()
        return {
            'boot_time_str': time_of_boot.strftime('%Y-%m-%d %H:%M:%S'),
            'boot_timestamp': time_of_boot.timestamp(),
            'elapsed_seconds': round(elapsed_seconds, 2),
            'elapsed_readable': readable_time(elapsed_seconds)
        }

    registry = {
        'du': get_du,
        'temps': get_multiple_temperatures,
        'boot_time': get_boot_time
    }

    if data_type not in registry.keys():
        return make_json_response(code=522, data='wrong data type')

    return make_json_response(code=0, data=registry.get(data_type)())


app.run(port=9090)
