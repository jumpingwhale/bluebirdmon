# -*-coding:utf-8-*-

import csv
import configparser
try:
    import tweepy
except ImportError:
    print('[E] ImportError : Try \'pip install tweepy\'')


# 전역변수
CONFIG_FILE_NAME = 'config.ini'
CSV_FILE_NAME = 'archive.csv'


def main():

    # 결과 저장을 위해 CSV 파일을 설정한다
    fp = open(CSV_FILE_NAME, 'a+', encoding='utf-8', newline='')  # 기존파일 뒤부터 쓰기
    wr = csv.writer(fp)

    # 설정파일을 가져온다
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_NAME)

    # 각종 키 및 팔로잉 중인 친구 목록을 가져온다
    CONSUMER_KEY = config['Twitter']['CONSUMER_KEY']
    CONSUMER_SECRET = config['Twitter']['CONSUMER_SECRET']
    ACCESS_TOKEN = config['Twitter']['ACCESS_TOKEN']
    ACCESS_TOKEN_SECRET = config['Twitter']['ACCESS_TOKEN_SECRET']
    FOLLOWINGS = [following.strip() for following in config['Twitter']['FOLLOWINGS'].split(',')]

    # tweepy 를 초기화한다
    try:
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)
    except Exception as e:
        print('[E] Initialize failed in tweepy : %s' % str(e))
        exit(1)

    # 각각의 유저에 대한 트윗을 얻어온다
    # .text 로 접근할 수 있고, .id 로 식별할 수 있다. created_at 은 생성날짜
    for following in FOLLOWINGS:
        print('[+] Retrieving %s\'s tweets' % following)
        timelines = api.user_timeline(screen_name=following, count=10)
        for timeline in timelines:
            row = [timeline.created_at, timeline.id, timeline.text.encode('utf8')]
            wr.writerow(row)

    fp.close()

if __name__ == '__main__':
    main()
