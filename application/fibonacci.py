import math

class CacheError(Exception):
  """  Exception of cache """
  def __init__(self, message):
    # Call the base class constructor with the parameters it needs
    super().__init__(message)

class ParamsError(Exception):
  """  Exception of parameters"""
  def __init__(self, message):
    # Call the base class constructor with the parameters it needs
    super().__init__(message)

class Fibonacci(object):
  """ Class to retrieve Fibonacci number or sequence

    Attributes:
      get_number: return a single Fibonacci number
      get_sequence: return a sequence of Fibonacci number
  """

  def __init__(self, cache=None, max_fibo_cached=1, max_fibo_layer=20):
    """ initialize members

    Args:
      cache (:obj, optional): global/distributed cache to cache Fibonacci numbers
      max_fibo_cached (int, optional): index of the maximum Fibonacci number in the cache.
          If Fibonacci(n) is cahed, all Fibonacci(k) (where, 0 <= k < n) should also be 
          in cached.
      max_fibo_layer (int, optional): The parameter to control the maximum Fibonacci 
          parameter that we can support: 2 power of ( log2(self.__max_fibo_cached) + self.__max_fibo_layer)
    """
    self.__cache = cache
    self.__max_fibo_cached = max_fibo_cached
    self.__max_fibo_layer = max_fibo_layer
    self.__map = {0: 0, 1: 1} # local cache for get_number()

  def get_number(self, n):
    """Return a Fibonacci number

    Args:
      n (int): index of the required Fibonacci number
  
    Returns:
      int: Fibonacci number 

    Raises:
      ParamsError: If anyone of parameters (n, offset, limit) is invalid
      CacheError: If cache behaves abnormally or Fibonacci number 
          retrieved from cached is not an integer
    """
    # validate parameters
    if (n < 0):
      raise ParamsError("Invalide parameter: 'n' should not be negative.")

    # return directly from map
    if n in self.__map:
      return self.__map[n]

    # verify if input parameter is too large to calculate Fibonacci number
    layer = math.ceil(math.log2(n)) - math.ceil(math.log2(self.__max_fibo_cached))
    if layer > self.__max_fibo_layer:
      fibo_limit = math.pow(2, math.log2(self.__max_fibo_cached) + self.__max_fibo_layer)
      raise ParamsError("The Fibonacci parameter is too larger. For now, the limit is %d" % (fibo_limit))
    
    # Fibonacci number should either be in cached or be returned directly
    if (n <= self.__max_fibo_cached):
      if self.__cache:
        fib = self.__cache.get(str(n))
        if fib:
          try:
            return int(fib)
          except ValueError:
            raise CacheError("Invalid Fibonacci number retrieved from cached. key=%s, value=%s" % (str(n), fib))
        else:
          raise CacheError("Miss cache while it should not. max_fibo_cached=%d, n=%s" % (self.__max_fibo_cached, str(n)))
      else:
          raise CacheError("There is no cache while max_fibo_cached is %d" % (self.__max_fibo_cached))

    # Calculate Fibonacci with log(n) time complexity
    else:
      if(n & 1) : # n is odd
        k = (n + 1) // 2
        fib = (self.get_number(k) * self.get_number(k) + self.get_number(k-1) * self.get_number(k-1))
      else :  # n is even
        k = n // 2
        fib = (2*self.get_number(k-1) + self.get_number(k)) * self.get_number(k)

      # store in map
      self.__map[n] = fib
      return fib

  def get_sequence(self, n, offset=0, limit=100):
    """Return a sequence of Fibonacci numbers

    Args:
      n (int): input parameter of Fibonacci(n) function
      offset (int): For pagination purpose. Indicates the offset of the 
          first Fibonacci number returned to client. Default value is 0. 
      limit (int): For pagination purpose. Indicates the max number of 
          Fibonacci number that can return to client. Default value is 100.
  
    Returns:
      tuple: Fibonacci number sequence

    Raises:
      ValueError: If offset is not in the range of [0, n]
    """
    # validate parameters
    if (offset < 0) or (offset > n):
      raise ParamsError("'offset' parameter should be in the range of [0, %d]" % (n))

    if (limit <= 0):
      raise ParamsError("'limit' parameter should be a positive integer")

    seq = []
    for i in range(0, limit):
      if (offset + i) > n:
        break
      if (i <= 1):
        # calculate the first two number by calling get_number()
        seq.append(self.get_number(offset + i))
      else:
        # calculate the rest from previous numbers
        seq.append(seq[i-2] + seq[i-1])
    return tuple(seq)
