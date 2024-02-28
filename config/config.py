class Config(object):
    TESTING = True
    DEBUG=True
    PASS_LOGIN_REQUIRED = False
    
    HOST="0.0.0.0"
    PORT=8825

    # jwt  
    
    # cors
    # CORS_RESOURCES={r"*": {"origins": ["*"]}}
    
    # 
    JSON_AS_ASCII=False

    # default data directory in container
    RESULT_STORAGE = "result/"


class Version(object):
    whisper_version = "20231117"
    echospeak_version = "v0.1"