

if __name__ == '__main__':

    from melo.api import TTS
    device = 'auto'
    models = {
        'KR': TTS(language='KR', device=device),
    }