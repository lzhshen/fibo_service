from memcache import Client

class CacheMgr(object):
  def __init__(self, servers=["127.0.0.1:11211"]):
    self.__mc = Client(servers)
    pass

  def tearDown(self):
    self.__mc.flush_all()
    self.__mc.disconnect_all()

  def get(self, key):
    val = self.__mc.get(key)
    return val

  def set(self, key, val):
    # TODO: noreply setting
    self.__mc.set(key, val)
