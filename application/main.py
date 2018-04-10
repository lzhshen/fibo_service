from flask import jsonify, request, Flask
from werkzeug.contrib.fixers import ProxyFix
from application.fibonacci import Fibonacci 
from application.pagination import RespData
import logging

# TODO: make it as configurable parameters
MAX_LIMIT = 1000

app = Flask(__name__)

# logging setting
gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.DEBUG)

def gen_response(msg, status_code):
  response = jsonify(message = msg)
  response.status_code = status_code
  return response

@app.route('/')
def index():
  return "Fibonacci webservice"

@app.errorhandler(404)
def page_not_found(e):
  return gen_response("page is not found", 404)

@app.route('/api/fibonacci/<int:n>')
def fibonacci(n):
  offset = 0
  limit = 100
  # Validate parameters
  offset_str = request.args.get('offset')
  limit_str = request.args.get('limit')
  # validate offset parameter
  if offset_str:
    msg = "'offset' should be an integer and be in the range of [0, %d]." % (n)
    try:
      offset = int(offset_str)
      if (offset < 0) or (offset > n):
        return gen_response(msg, 403)
    except ValueError:
        return gen_response(msg, 403)

  # validate offset parameter
  if limit_str:
    msg = "'limit' should be an integer and be in the range of (0, %d]." % (MAX_LIMIT)
    try:
      limit = int(limit_str)
      if (limit <= 0) or (limit > MAX_LIMIT): 
        return gen_response(msg, 403)
    except ValueError:
        return gen_response(msg, 403)

  # Get fibonacci number sequence
  try:
    fibo = Fibonacci()
    seq = fibo.get_sequence(n, offset, limit)
    resp_data = RespData(n, offset, limit, seq, '/api/fibonacci')
    response = jsonify(results=resp_data.data())
    response.status_code = 200
  except Exception as e:
    app.logger.exception(str(e))
    response = jsonify(message = str(e))
    response.status_code = 403
  return response

if __name__ == '__main__':
  app.run()
