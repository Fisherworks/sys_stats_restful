from microdot import Microdot
from psutil import disk_usage, sensors_temperatures

app = Microdot()

@app.route('/stats')
def stats(request):
    """ gather os/hw stats as needed """
    du = disk_usage('/')
    temps = sensors_temperatures()
    return {
        'du': {
            'free_size': round(du.free/(2**20), 2),
            'free_rate': round(100 - float(du.percent), 2)
        },
        'temps': {k: {'curr': round(v[0].current, 2), 'crit': round(v[0].critical, 2)} for k, v in temps.items() if v}
    }

app.run(port=9090)
