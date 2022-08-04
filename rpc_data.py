import json
import execjs
import requests
from logger.log import logger
from lxml import etree


class Tiktok:
    def __init__(self):
        """
            初始化一些参数
        """
        self.user_name = ""
        self.url = "http://127.0.0.1:5620/business-demo/invoke?group=tiktok&action=getData&userName={}&page=0"
        self.next_url = "http://127.0.0.1:5620/business-demo/invoke?group=tiktok&action=getData&userName={}&page=1&params={}"

    def send_content(self, data):
        logger.info("发送kafka")

    @staticmethod
    def get_params(cursor_, sec_uid, fp):
        js = open("sheep.js").read()
        js = execjs.compile(js)
        result = js.call("get_x_tt_params", cursor_, sec_uid, fp)
        return result

    @staticmethod
    def send_request(url):
        response = requests.get(url=url).json()
        return response

    @staticmethod
    def parse_user(data, user_name):
        user_data = data["users"][user_name[1:]]
        # id
        user_id = user_data.get("id")
        # 名字
        unique_id = user_data.get("uniqueId")
        # 名字
        nick_name = user_data.get("nickname")
        # 头像链接， 有过期时间
        avatar_larger = user_data.get("avatarLarger")
        # 简介
        desc = user_data.get("signature")
        # 用户唯一id  secUid
        sec_uid = user_data.get("secUid")
        # linktr链接
        link = user_data.get("bioLink").get("link")
        follow_data = data["stats"][user_name[1:]]
        # 粉丝数量
        follower_count = follow_data.get("followerCount")
        # 关注数量
        following_count = follow_data.get("followingCount")
        # 点赞数量
        heart_count = follow_data.get("heartCount")
        # 视频数量
        video_count = follow_data.get("videoCount")
        return {
            "user_id": user_id,
            "unique_id": unique_id,
            "nick_name": nick_name,
            "avatar_larger": avatar_larger,
            "desc": desc,
            "sec_uid": sec_uid,
            "link": link,
            "follower_count": follower_count,
            "following_count": following_count,
            "heart_count": heart_count,
            "video_count": video_count,
        }

    @staticmethod
    def parse_video(data):
        videos = []
        for value in data:
            # 时间戳
            create_time = value.get("createTime")
            # 视频简介
            video_desc = value.get("desc")
            # 作者
            author = value.get("author")
            if isinstance("dict", author):
                author = author.get("uniqueId")
                author_id = author.get("id")
                author_sec_uid = author.get("authorSecId")
            else:
                # 作者id
                author_id = value.get("authorId")
                # 作者的secUid
                author_sec_uid = value.get("authorSecId")
            # 视频id
            video_id = value.get("video").get("id")
            # 封面图片
            cover = value.get("video").get("cover")
            # 视频链接
            download_addr = value.get("video").get("downloadAddr")
            # 音乐链接
            music_link = value.get("music").get("playUrl")
            # 音乐id
            music_id = value.get("music").get("id")
            # 音乐标题
            music_title = value.get("music").get("title")
            # 点赞数量
            diggCount = value.get("stats").get("diggCount")
            # 分享数量
            shareCount = value.get("stats").get("shareCount")
            # 评论数量
            commentCount = value.get("stats").get("commentCount")
            # 播放数量
            playCount = value.get("stats").get("playCount")

            video_data = {
                "video": {"video_desc": video_desc, "create_time": create_time, "video_id": video_id, "cover": cover,
                          "download_addr": download_addr, "diggCount": diggCount, "shareCount": shareCount,
                          "commentCount": commentCount, "playCount": playCount},
                "music": {"music_link": music_link, "music_id": music_id, "music_title": music_title},
                "author": {"author": author, "author_id": author_id, "author_sec_uid": author_sec_uid}
            }
            videos.append(video_data)
        return videos

    def parse_next(self, cursor, sec_uid, user_name):
        params = self.get_params(cursor, sec_uid, "")
        logger.info("请求下一页")
        next_url = self.next_url.format(user_name, params)
        response = self.send_request(next_url)
        item_list = response["itemList"]
        next_video_data = self.parse_video(item_list)
        result = {"video": next_video_data}
        self.send_content(result)
        # 翻页参数
        cursor = response["cursor"]
        if cursor:
            # 递归请求下一页
            self.parse_next(cursor, sec_uid, user_name)

    def parse_data(self, data, user_name):
        html = etree.HTML(data)
        index_data = html.xpath("//script[@id='SIGI_STATE']/text()")
        if index_data:
            json_data = json.loads(index_data[0])
            # user info
            user_item = json_data["UserModule"]
            user_data = self.parse_user(user_item, user_name)
            # video info
            video_items = json_data["ItemModule"]
            video_values = list(video_items.values())
            video_data = self.parse_video(video_values)
            result = {"user": user_data, "video": video_data}
            self.send_content(result)

            # 翻页参数
            cursor = json_data["ItemList"]["user-post"]["cursor"]
            # 用户secUid
            sec_uid = json_data["UserPage"]["secUid"]
            if cursor:
                self.parse_next(cursor, sec_uid, user_name)

    def main(self):
        logger.info("-----开始采集-----")
        url = tiktok.url.format(self.user_name)
        response = Tiktok.send_request(url)
        data = response.get("data")
        if not data:
            logger.info("rpc未获取到数据")
            return
        tiktok.parse_data(data, self.user_name)


if __name__ == '__main__':
    tiktok = Tiktok()
    tiktok.main()
