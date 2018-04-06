
class RespData:
  def __init__(self, n, offset, limit, fibo_seq, url_prefix):
    self.__n = n
    self.__offset = offset
    self.__limit = limit
    self.__fibo_seq = fibo_seq
    self.__url_prefix = url_prefix

  def data(self):
    pagination = {
      'offset': self.__offset,
      'limit': self.__limit,
      'total': self.__n + 1
    }
    next_url = 'n/a' 
    next_offset = self.__offset + self.__limit
    if next_offset <= self.__n:
      next_url = "%s/%d?offset=%d&limit=%d" % (self.__url_prefix, 
                                               self.__n, 
                                               next_offset,
                                               self.__limit)
    data = {
      'pagination': pagination,
      'data': self.__fibo_seq,
      'links': {
        'next': next_url
      }
    }
    return data

