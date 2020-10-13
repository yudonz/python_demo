from csdn import article
from csdn import video

if __name__ == '__main__':
    print("请输入课程编号:")
    number = int(input())
    url = 'https://gate.lagou.com/v1/neirong/kaiwu/getCourseLessons?courseId={}'.format(number)
    video = video.LaGou_spider(url)
    video.main()
    article = article.LaGou_Article_Spider(url)
    article.main()
