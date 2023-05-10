from microdot import Microdot
from datetime import datetime
from psutil import disk_usage, sensors_temperatures, boot_time

app = Microdot()


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


@app.route('/stats')
def stats(request):
    """ gather os/hw stats as needed """
    du = disk_usage('/')
    temps = sensors_temperatures()
    time_of_boot = datetime.fromtimestamp(boot_time())
    elapsed = datetime.now() - time_of_boot
    return {
        'du': {
            'free_size': round(du.free/(2**20), 2),
            'free_rate': round(100 - float(du.percent), 2)
        },
        'temps': {k: {'curr': round(v[0].current, 2), 'crit': round(v[0].critical, 2)}
                  for k, v in temps.items() if v},
        'boot_time': {
            'boot_time': time_of_boot.strftime('%Y-%m-%d %H:%M:%S'),
            'boot_timestamp': time_of_boot.timestamp(),
            'elapsed_seconds': round(elapsed.total_seconds(), 2),
            'elapsed_readable': readable_time(elapsed.total_seconds())
        }
    }


app.run(port=9090)
