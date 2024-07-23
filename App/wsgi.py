from websocketTest import app

if __name__ == "__main__":
    app.run()

#formatter = logging.Formatter(  # pylint: disable=invalid-name
 #   '%(asctime)s %(levelname)s %(process)d ---- %(threadName)s  '
 #   '%(module)s : %(funcName)s {%(pathname)s:%(lineno)d} %(message)s','%Y-%m-%dT%H:%M:%SZ')

#handler = StreamHandler()
#handler.setFormatter(formatter)

#app.logger.setLevel(logging.DEBUG)
#app.logger.addHandler(handler)
#app.logger.removeHandler(default_handler)
