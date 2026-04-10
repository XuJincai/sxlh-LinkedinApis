import json
import re

import requests
from bs4 import BeautifulSoup
import uuid

from builder.auth import LinkAuth
from builder.header import HeaderBuilder
from builder.params import ParamsBuilder
from utils.link_utils import splice_url, generate_trackingId


class LinkApi:
    base_url = "https://www.rootdata.com"

    def get_search_query_id(self, auth, proxies=None):
        url = "https://www.linkedin.com/"
        headers = HeaderBuilder.build_common_header()
        response = requests.get(url, headers=headers.get(), cookies=auth.cookie)
        res_text = response.text
        soup = BeautifulSoup(res_text, 'html.parser')
        scripts = soup.select('script[nonce]')
        for script in scripts:
            srcs = re.findall(r' src="(.*?)"', str(script))
            if len(srcs) > 0:
                src = srcs[0]
                js_res = requests.get(src, headers=headers.get(), cookies=auth.cookie, proxies=proxies)
                js_res_text = js_res.text
                if 'graphql-queries/queries/search/search-cluster-collection.graphql' in js_res_text:
                    query_id = re.findall(r'define\("graphql-queries/queries/search/search-cluster-collection\.graphql",.*?id:"(.*?)",typeName', js_res_text, re.S)
                    return query_id[0]

    def search_some(self, start, query, query_id, auth, proxies=None):
        url = "https://www.linkedin.com/voyager/api/graphql"
        params = {
            "variables": f"(start:{start},origin:GLOBAL_SEARCH_HEADER,query:(keywords:{query},flagshipSearchIntent:SEARCH_SRP,queryParameters:List((key:resultType,value:List(ALL))),includeFiltersInResponse:false))",
            "queryId": query_id
        }
        url = splice_url(url, params)
        headers = HeaderBuilder.build_request_header(auth)
        response = requests.get(url, headers=headers.get(), cookies=auth.cookie, proxies=proxies)
        res_json = response.json()
        return res_json

    def get_send_msg_info(self, url, auth, proxies=None):
        headers = HeaderBuilder.build_common_header()
        response = requests.get(url, headers=headers.get(), cookies=auth.cookie, proxies=proxies)
        res_text = response.text
        mailboxUrn = re.findall(r'\*profile&quot;:&quot;(.*?)&quot;,&quot;', res_text)[0]
        hostRecipientUrns = re.findall(r'\*pageMailbox&quot;:&quot;(.*?)&quot;,&quot;', res_text)[0]
        return res_text, mailboxUrn, hostRecipientUrns

    def send_msg(self, home_url, msg, auth, proxies=None):
        user_info, mailboxUrn, hostRecipientUrns = self.get_send_msg_info(home_url, auth, proxies)
        url = "https://www.linkedin.com/voyager/api/voyagerMessagingDashMessengerMessages"
        params = {
            "action": "createMessage"
        }
        uuid_ = uuid.uuid4()
        uuid_ = str(uuid_)
        data = {
            "message": {
                "body": {
                    "attributes": [],
                    "text": msg
                },
                "originToken": uuid_,
                "renderContentUnions": []
            },
            "mailboxUrn": mailboxUrn,
            "trackingId": generate_trackingId(uuid_),
            "dedupeByClientGeneratedToken": False,
            "hostRecipientUrns": [
                hostRecipientUrns
            ],
            "hostMessageCreateContent": {
                "com.linkedin.voyager.dash.messaging.MessageCreateContent": {
                    "messageCreateContentUnion": {
                        "pagesMessaging": {
                            "pageMailboxConversationTopicUrn": "urn:li:fsd_pageMailboxConversationTopic:7"
                        }
                    }
                }
            }
        }
        data = json.dumps(data, separators=(',', ':'))
        headers = HeaderBuilder.build_request_header(auth)
        response = requests.post(url, headers=headers.get(), cookies=auth.cookie, params=params, data=data, proxies=proxies)
        res_json = response.json()
        return res_json

    def get_user_info(self, user_url, auth, proxies=None):
        # https://www.linkedin.com/in/davidailsworth/
        if user_url.endswith('/'):
            user_id = user_url.split('/')[-2]
        else:
            user_id = user_url.split('/')[-1]
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'priority': 'u=0, i',
            'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        }
        response = requests.get(user_url, headers=headers, proxies=proxies, cookies=auth.cookie)
        res_text = response.text
        x_li_uuid = re.findall(r'{"x-li-uuid":"(.*?)"}', res_text)[0]
        x_li_uuid = x_li_uuid.encode('utf-8').decode('unicode_escape')
        fsd_profile = re.findall(r'urn:li:fsd_memberRelationship:(.*?),', res_text)[0].replace('&quot;', '')
        js_id = re.findall(r'src="https://static.licdn.com/aero-v1/sc/h/(.*?)" data-fastboot-src="/assets/vendor.js"', res_text)[0]
        headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'origin': 'https://www.linkedin.com',
            'pragma': 'no-cache',
            'priority': 'u=1',
            'referer': 'https://www.linkedin.com/',
            'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'script',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        }
        response = requests.get(f'https://static.licdn.com/aero-v1/sc/h/{js_id}', headers=headers)
        js_text = response.text

        # 获取个人简介
        desc_queryId = re.findall(r'define\("graphql-queries/queries/profile/identityDashProfileCards/profile-cards-by-initial-cards\.graphql",.*?id:"(.*?)",typeName', js_text, re.S)[0]
        headers = {
            'Host': 'www.linkedin.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'sec-ch-ua-platform': '"Windows"',
            'x-li-track': '{"clientVersion":"1.13.33379","mpVersion":"1.13.33379","osName":"web","timezoneOffset":8,"timezone":"Asia/Shanghai","deviceFormFactor":"DESKTOP","mpName":"voyager-web","displayDensity":1,"displayWidth":2560,"displayHeight":1440}',
            'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            'csrf-token': re.findall(r'JSESSIONID="(.*?)"', auth.cookie_str)[0],
            'sec-ch-ua-mobile': '?0',
            'x-restli-protocol-version': '2.0.0',
            'x-li-page-instance': f'urn:li:page:d_flagship3_profile_view_base;{x_li_uuid}',
            'x-li-lang': 'zh_CN',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
            'accept': 'application/vnd.linkedin.normalized+json+2.1',
            'x-li-pem-metadata': 'Voyager - Profile=profile-tab-initial-cards',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': user_url,
            'accept-language': 'zh-CN,zh;q=0.9',
            'priority': 'u=1, i',
        }
        url = f'https://www.linkedin.com/voyager/api/graphql?includeWebMetadata=true&variables=(profileUrn:urn%3Ali%3Afsd_profile%3A{fsd_profile})&queryId={desc_queryId}'
        response = requests.get(url, headers=headers, proxies=proxies, cookies=auth.cookie)
        res_json = response.json()
        desc = res_json["included"][14]["topComponents"][1]["components"]["textComponent"]["text"]["text"]

        # 获取最上面的个人简介
        top_desc_queryId = re.findall(r'define\("graphql-queries/queries/profile/identityDashProfiles/top-card-supplementary-query\.graphql",.*?id:"(.*?)",typeName', js_text, re.S)[0]
        headers = {
            'Host': 'www.linkedin.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'sec-ch-ua-platform': '"Windows"',
            'x-li-track': '{"clientVersion":"1.13.33379","mpVersion":"1.13.33379","osName":"web","timezoneOffset":8,"timezone":"Asia/Shanghai","deviceFormFactor":"DESKTOP","mpName":"voyager-web","displayDensity":1,"displayWidth":2560,"displayHeight":1440}',
            'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            'csrf-token': re.findall(r'JSESSIONID="(.*?)"', auth.cookie_str)[0],
            'sec-ch-ua-mobile': '?0',
            'x-restli-protocol-version': '2.0.0',
            'x-li-page-instance': f'urn:li:page:d_flagship3_profile_view_base;{x_li_uuid}',
            'x-li-lang': 'zh_CN',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
            'accept': 'application/vnd.linkedin.normalized+json+2.1',
            'x-li-pem-metadata': 'Voyager - Profile=profile-top-card-supplementary',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': user_url,
            'accept-language': 'zh-CN,zh;q=0.9',
            'priority': 'u=1, i',
        }
        url = f'https://www.linkedin.com/voyager/api/graphql?includeWebMetadata=true&variables=(vanityName:{user_id})&queryId={top_desc_queryId}'
        response = requests.get(url, headers=headers, proxies=proxies, cookies=auth.cookie)
        res_json = response.json()
        top_desc = res_json["included"][4]["headline"]
        first_name = res_json["included"][4]["firstName"]
        last_name = res_json["included"][4]["lastName"]
        user_name = f"{first_name} {last_name}"
        res = {
            "user_name": user_name,
            "user_id": user_id,
            "desc": desc,
            "top_desc": top_desc
        }
        return res


if __name__ == '__main__':
    linkAuth = LinkAuth()
    cookies_str = r''
    linkAuth.perepare_auth(cookies_str)
    linkApi = LinkApi()


    # query_id = linkApi.get_search_query_id(linkAuth)
    # print(query_id)
    # start = 0
    # query = 'David Ailsworth'
    # res_json = linkApi.search_some(start, query, query_id, linkAuth)
    # print(json.dumps(res_json))

    user_url = 'https://www.linkedin.com/in/davidailsworth/'
    user_url = 'https://www.linkedin.com/in/jordan-bilyeu-a026b440'
    user_info = linkApi.get_user_info(user_url, linkAuth)
    print(user_info)

    # home_url = 'https://www.linkedin.com/school/getsmarter/posts/?feedView=all'
    # home_url = 'https://www.linkedin.com/company/farmoutph/'
    # msg = 'testtesttesttesttesttesttesttest'
    # res_json = linkApi.send_msg(home_url, msg, linkAuth)
    # print(json.dumps(res_json, indent=4))
