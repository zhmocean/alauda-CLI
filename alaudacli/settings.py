import os


ALAUDACFG = os.path.expanduser('~/.alaudacfg')


API_ENDPOINTS = {
    'cn': 'https://api.alauda.cn/v1/',
    'io': 'https://api.alauda.io/v1/'
}

S3_BUCKET = 'build-file-upload'
AWS_REGION_NAME = 'cn-north-1'

BUILD_REPO_TYPE = {
    'file': 'FILE',
    'code_repo': 'CODE_REPO',
    'not_automated': 'NOT_AUTOMATED'
}
