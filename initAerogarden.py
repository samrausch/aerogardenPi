import redis
import time

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

r.flushdb()

r.set('pumpPIN', 22)
r.set('pumpState', 1)
r.set('pumpOnTime', 300)
r.set('pumpOffTime', 1200)
r.set('pumpLastAction', time.time())
r.set('pumpTimer', 300)

r.set('lightPIN', 27)
r.set('lightState', 1)
r.set('lightOnTime', 3600)
r.set('lightOffTime', 7200)
r.set('lightLastAction', time.time())
r.set('lightTimer', 900)

r.set('buttonPIN', 26)
