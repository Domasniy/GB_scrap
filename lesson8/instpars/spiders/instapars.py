import scrapy
from scrapy.http import HtmlResponse
from instpars.items import InstparsItem
import re
import json
from urllib.parse import urlencode
from copy import deepcopy

class InstaparsSpider(scrapy.Spider):
    name = 'instapars'
    allowed_domains = ['instagram.com']
    start_urls = ['https://instagram.com/']
    insta_login = 'пользователь'
    insta_pwd = 'пароль'
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    parse_user = ['salondub','afinaschool']     #Пользователь, у которого собираем посты. Можно указать список

    graphql_url = 'https://www.instagram.com/graphql/query/?'
    followers_hash = 'c76146de99bb02f6415203be841dd25a'
    follow_hash = 'd04b0a864b4b54837c0d870b0e77e076'

    def parse(self, response:HtmlResponse):             #Первый запрос на стартовую страницу
        csrf_token = self.fetch_csrf_token(response.text)   #csrf token забираем из html
        yield scrapy.FormRequest(                   #заполняем форму для авторизации
            self.inst_login_link,
            method='POST',
            callback=self.user_parse,
            formdata={'username':self.insta_login, 'enc_password':self.insta_pwd},
            headers={'X-CSRFToken':csrf_token}
        )

    def user_parse(self, response:HtmlResponse):
        j_body = json.loads(response.text)
        if j_body['authenticated']:
            for user in self.parse_user:                
                yield response.follow(                  
                    f'/{user}',
                    callback= self.user_data_parse,
                    cb_kwargs={'username':user}
                )

    def user_data_parse(self, response:HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)       #Получаем id пользователя
        variables={'id':user_id,                                    #Формируем словарь для передачи даных в запрос
                   'first':50}                                      #12 постов. Можно больше (макс. 50)
        url_followers = f'{self.graphql_url}query_hash={self.followers_hash}&{urlencode(variables)}'    #Формируем ссылку для получения данных о постах
        yield response.follow(
            url_followers,
            callback=self.user_followers_parse,
            cb_kwargs={'username':username,
                       'user_id':user_id,
                       'variables':deepcopy(variables)}         #variables ч/з deepcopy во избежание гонок
        )

        url_follow = f'{self.graphql_url}query_hash={self.follow_hash}&{urlencode(variables)}'
        yield response.follow(
            url_follow,
            callback=self.user_follow_parse,
            cb_kwargs={'username':username,
                       'user_id':user_id,
                       'variables':deepcopy(variables)}         #variables ч/з deepcopy во избежание гонок
        ) 

    def user_followers_parse(self, response:HtmlResponse,username,user_id,variables):   #Принимаем ответ. Не забываем про параметры от cb_kwargs
        j_data = json.loads(response.text)
        # Блок обработки followers
        page_info_followers = j_data.get('data').get('user').get('edge_followed_by').get('page_info')
        if page_info_followers.get('has_next_page'):                                          #Если есть следующая страница
            variables['after'] = page_info_followers['end_cursor']                            #Новый параметр для перехода на след. страницу
            url_posts = f'{self.graphql_url}query_hash={self.followers_hash}&{urlencode(variables)}'
            yield response.follow(
                url_posts,
                callback=self.user_followers_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'variables': deepcopy(variables)}
            )
        followers = j_data.get('data').get('user').get('edge_followed_by').get('edges')     # список followers
        for follow in followers:                                                                      #Собираем данные по каждому follower
            item = InstparsItem(
                user_id = user_id,
                username = username,
                follower_username = follow['node']['username'],
                follower_full_name = follow['node']['full_name'],
                follower_photo = follow['node']['profile_pic_url'],
                follow_by = True
            )
            yield item 

    def user_follow_parse(self, response:HtmlResponse,username,user_id,variables):   #Принимаем ответ. Не забываем про параметры от cb_kwargs
        j_data = json.loads(response.text)
       # Блок обработки follow
                        
        page_info_follow = j_data.get('data').get('user').get('edge_follow').get('page_info')
        if page_info_follow.get('has_next_page'):                                          #Если есть следующая страница
            variables['after'] = page_info_follow['end_cursor']                            #Новый параметр для перехода на след. страницу
            url_posts = f'{self.graphql_url}query_hash={self.follow_hash}&{urlencode(variables)}'
            yield response.follow(
                url_posts,
                callback=self.user_follow_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'variables': deepcopy(variables)}
            )
        follow_me = j_data.get('data').get('user').get('edge_follow').get('edges')     # список followers
        for follow in follow_me:                                                                      #Собираем данные по каждому follower
            item = InstparsItem(
                user_id = user_id,
                username = username,
                follower_username = follow['node']['username'],
                follower_full_name = follow['node']['full_name'],
                follower_photo = follow['node']['profile_pic_url'],
                follow_by = False
            )
            yield item    


    #Получаем токен для авторизации
    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    #Получаем id желаемого пользователя
    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')