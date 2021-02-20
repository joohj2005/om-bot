import discord
client = discord.Client()
import requests
import urllib.request
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import os
import time
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--window-size=1024,768')
    options.add_argument("--disable-gpu")
    global driver_search
    driver_search = webdriver.Chrome(executable_path='/app/.chromedriver/bin/chromedriver', options=options)
    driver_search.get("http://om.skhidc.kr/index.php")
    global driver_so
    global driver_sg
    global driver_mo
    driver_so = webdriver.Chrome(executable_path='/app/.chromedriver/bin/chromedriver', options=options)
    driver_sg = webdriver.Chrome(executable_path='/app/.chromedriver/bin/chromedriver', options=options)
    driver_mo = webdriver.Chrome(executable_path='/app/.chromedriver/bin/chromedriver', options=options)
    driver_so.get(url='https://skhlist.com/server/79')
    driver_sg.get(url='https://skhlist.com/server/324')
    driver_mo.get(url='https://minelist.kr/servers/onemoon.skhidc.kr')
    print('ready')
    
@client.event
async def on_message(message):
    if message.author.bot:
        return None
    
    if message.content == "!일월 정보":

        embed=discord.Embed(title='일월 정보', color=0x00ff56)

        global driver_so
        global driver_mo

        version1 = driver_so.find_element_by_css_selector("body > div.container-fluid > section > div:nth-child(2) > div > div.col-lg-9.col-md-9 > div:nth-child(2) > div.posttext.pull-left > div.table-responsive > table:nth-child(1) > tbody > tr > td:nth-child(1)")
        version = version1.text
        address1 = driver_so.find_element_by_css_selector("body > div.container-fluid > section > div:nth-child(2) > div > div.col-lg-9.col-md-9 > div:nth-child(2) > div.posttext.pull-left > div.table-responsive > table:nth-child(1) > tbody > tr > td:nth-child(2)")
        address = address1.text
        users1 = driver_so.find_element_by_css_selector("body > div.container-fluid > section > div:nth-child(2) > div > div.col-lg-9.col-md-9 > div:nth-child(2) > div.posttext.pull-left > div.table-responsive > table:nth-child(2) > tbody > tr > td:nth-child(2)")
        users = users1.text
        vote_skh1 = driver_so.find_element_by_css_selector("body > div.container-fluid > section > div:nth-child(2) > div > div.col-lg-9.col-md-9 > div:nth-child(2) > div.posttext.pull-left > div.table-responsive > table:nth-child(2) > tbody > tr > td:nth-child(3)")
        vote_skh = vote_skh1.text

        vote_mine1 = driver_mo.find_element_by_css_selector("body > div.container.wrap.ml-content > div.row > div > div.col-md-12.server-info.bottom.container-fluid > div:nth-child(1) > p.no-y")
        vote_mine = vote_mine1.text

        embed.add_field(name='버전', value=version, inline=True)
        embed.add_field(name='주소', value=address, inline=True)
        embed.add_field(name='접속자수', value=users, inline=False)
        embed.add_field(name='마인리스트 추천수', value=vote_mine, inline=True)
        embed.add_field(name='SKH리스트 추천수', value=vote_skh, inline=True)

        await message.channel.send(embed=embed)
    
    if message.content.startswith('!일월 랭킹'):

        ranking1 = message.content[7:9]
        page1 = message.content[10:len(message.content)]

        try:
            page = int(page1)

        except ValueError:
            await message.channel.send('!일월 랭킹 <일반 / 기문 / 만렙> <페이지>')

        else:
            pass

        finally:
            pass

        if (page >= 1 and page <=10):
            page = str(page1)

        else:
            page = '1'

        if ranking1 == "일반":
            ranking = "top"

        elif ranking1 == "기문":
            ranking = "top2"

        elif ranking1 == "만렙":
            ranking = "king"

        else:
            ranking = "일반"
            ranking = "top"

        info = ranking1+'랭킹'+page

        req = requests.get('http://om.skhidc.kr/level'+ranking+'.php'+'?page='+page)  
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')

        embed=discord.Embed(title=info, color=0x00ff56)

        try:
            table = soup.find('table', {'class': 'table table-bordered'})
            trs = table.find_all('tr')
            for idx, tr in enumerate(trs):
                if idx > 0:
                    tds = tr.find_all('td')
                    ranking = tds[0].text.strip()
                    nickname = tds[1].text.strip()
                    job = tds[3].text.strip()
                    level = tds[4].text.strip()
                    embed.add_field(name=ranking, value='닉네임: ' + nickname + ' | 직업: ' + job + ' | 레벨: ' + level, inline=False)
                    
        except AttributeError:
            info = ranking1+'랭킹 '+page+' (기록없음)'
            embed=discord.Embed(title=info, color=0x00ff56)

        await message.channel.send(embed=embed)
    
    if message.content.startswith('!일월 괴영'):

        season1 = message.content[7:8]

        try:
            season = int(season1)

        except ValueError:
            await message.channel.send('!일월 괴영 <시즌> <직업>')

        else:
            pass

        finally:
            pass
                
        job1 = message.content[9:len(message.content)]

        if job1 == "검객":
            job = "swordman"

        elif job1 == "자객":
            job = "assassin"

        elif job1 == "궁사":
            job = "archer"

        elif job1 == "진사":
            job = "jinsa"

        elif job1 == "닌자":
            job = "ninja"

        elif job1 == "월사":
            job = "axewarrier"

        elif job1 == "법사":
            job = "magician"

        elif job1 == "창술사":
            job = "spearman"

        else:
            job = "swordman"
            job1 = "검객"

        if season == 7:
            season = str(season1)
            req = requests.get('http://om.skhidc.kr/carnivaltop.php?job='+job)  
            html = req.text
            soup = BeautifulSoup(html, 'html.parser')
            info = message.content[4:8]+' '+job1

        elif season >= 8:
            season = str(season1)
            req = requests.get('http://om.skhidc.kr/carnival_season.php?job='+job,'&season=1')  
            html = req.text
            soup = BeautifulSoup(html, 'html.parser')
            info = message.content[4:7] + "1 " + job1
                
        else:
            season = str(season1)
            req = requests.get('http://om.skhidc.kr/carnival_season.php?job='+job+'&season='+season)  
            html = req.text
            soup = BeautifulSoup(html, 'html.parser')
            info = message.content[4:7]+season1+' '+job1

        embed=discord.Embed(title=info, color=0x00ff56)

        table = soup.find('table', {'class': 'table table-bordered'})
        trs = table.find_all('tr')
        for idx, tr in enumerate(trs):
            if idx > 0:
                tds = tr.find_all('td')
                ranking = tds[0].text.strip()
                nickname = tds[1].text.strip()
                score = tds[3].text.strip()
                embed.add_field(name=ranking, value='닉네임: ' + nickname + ' | 점수: ' + score, inline=False)

        await message.channel.send(embed=embed)

    if message.content.startswith('!일월 검색'):

        Name = message.content[7:len(message.content)]

    try:
        global driver_search
        chrome = driver_search.find_element_by_xpath('//*[@id="myNavbar"]/ul/li[1]/a')
        if len(chrome.text) >= 1:
            
            search_box = driver_search.find_element_by_class_name('form-control')
            search_box.send_keys(Name)
            search_box.send_keys(Keys.RETURN)
            
        else:
            driver_search.get(url='http://om.skhidc.kr/')
            search_box = driver_search.find_element_by_class_name('form-control')
            search_box.send_keys(Name)
            search_box.send_keys(Keys.RETURN)
            
    except NoSuchElementException:
        driver_search.get(url='http://om.skhidc.kr/')
        search_box = driver_search.find_element_by_class_name('form-control')
        search_box.send_keys(Name)
        search_box.send_keys(Keys.RETURN)
    embed=discord.Embed(title=Name, color=0x00ff56)
    try:
        elem = driver_search.find_element_by_xpath('/html/body/table/tbody/tr/th[1]/div')
        if len(elem.text) >= 1:
            
            card1 = driver_search.find_element_by_xpath('/html/body/table/tbody/tr/th[1]/div')
            card1_data = card1.text
            embed.add_field(name="캐릭터1", value=card1_data, inline=True)
            
        else:
            embed.add_field(name="캐릭터1", value="없음", inline=True)
    except NoSuchElementException:
        embed.add_field(name="캐릭터1", value="없음", inline=True)
    try:
        elem = driver_search.find_element_by_xpath('/html/body/table/tbody/tr/th[2]/div')
        if len(elem.text) >= 1:
            
            card2 = driver_search.find_element_by_xpath('/html/body/table/tbody/tr/th[2]/div')
            card2_data = card2.text
            embed.add_field(name="캐릭터2", value=card2_data, inline=True)
            
        else:
            embed.add_field(name="캐릭터2", value="없음", inline=True)
    except NoSuchElementException:
        embed.add_field(name="캐릭터2", value="없음", inline=True)
    try:
        elem = driver_search.find_element_by_xpath('/html/body/table/tbody/tr/th[3]/div')
        if len(elem.text) >= 1:
            
            card3 = driver_search.find_element_by_xpath('/html/body/table/tbody/tr/th[3]/div')
            card3_data = card3.text
            embed.add_field(name="캐릭터3", value=card3_data, inline=False)
            
        else:
            embed.add_field(name="캐릭터3", value="없음", inline=False)
    except NoSuchElementException:
        embed.add_field(name="캐릭터3", value="없음", inline=False)
    try:
        elem = driver_search.find_element_by_xpath('/html/body/table/tbody/tr/th[4]/div')
        if len(elem.text) >= 1:
            
            card4 = driver_search.find_element_by_xpath('/html/body/table/tbody/tr/th[4]/div')
            card4_data = card4.text
            embed.add_field(name="캐릭터4", value=card4_data, inline=True)
            
        else:
            embed.add_field(name="캐릭터4", value="없음", inline=True)
    except NoSuchElementException:
        embed.add_field(name="캐릭터4", value="없음", inline=True)
    try:
        elem = driver_search.find_element_by_xpath('/html/body/table/tbody/tr/th[5]/div')
        if len(elem.text) >= 1:
            
            card5 = driver_search.find_element_by_xpath('/html/body/table/tbody/tr/th[5]/div')
            card5_data = card5.text
            embed.add_field(name="캐릭터5", value=card5_data, inline=True)
            
        else:
            embed.add_field(name="캐릭터5", value="없음", inline=True)
    except NoSuchElementException:
        embed.add_field(name="캐릭터5", value="없음", inline=True)
    
    
    await message.channel.send(embed=embed)
access_token = os.environ['BOT_TOKEN']
client.run(access_token)
