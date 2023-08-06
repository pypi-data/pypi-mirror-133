from rss.tensorflow import TensorFlowBlog
from rss.openai import OpenAI

OBSERVE_MAP = {
    'tensorflow': {
        'host':
        'https://blog.tensorflow.org/search?updated-max=2022-06-02T12:00:00-07:00&max-results=200&start=20&by-date=false',
        'url': 'https://blog.tensorflow.org',
        'parser': TensorFlowBlog
    },
    'openai': {
        'host': 'https://openai.com/blog/',
        'url': 'https://openai.com/blog/',
        'parser': OpenAI
    }
}

REDIS_MAP = {
    'host': 'ali_redis_host',
    'port': 'ali_redis_port',
    'pass': 'ali_redis_pass'
}