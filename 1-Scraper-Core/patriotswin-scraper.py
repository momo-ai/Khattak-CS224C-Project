from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import pandas as pd
import time

URL = 'https://patriots.win/top?sort=all'
"""
DIV - Main page (https://patriots.win/top?from=16aT36KFQA&sort=week)

<div class=“wrapper home panel”
	<div class =“container”
		<main class=“main
			<div class=“main-content post-list”
				<div class=“post mobile_guest” data-type=“post”
					<div class=“body”
						<div class=“top”
							<a href
<div class=“more”

DIV - Given Post

<article class=‘main-content’
	<div class=‘post’
		<div class=‘body’
			<div class=‘top’
				<a href text is TITLE
<div class=‘comment-section’
	<div class=“total” // text is Comments (NUM)
	<section class=‘comment-list’
		<div class=‘comment’ data-author=‘author’
			<div class=‘vote’
				<span class=‘count’ // could be useful metadata
			<div class=‘body’
				<div class=‘details’
					<div class=‘author’ // compile these is cool
				<div class=‘content’
					<p // contains content
			<div class=‘child’ // recursive case, child contains comment class which goes on
"""



# tot_comments = 0
# file = open('./patriots_win.csv', 'rb')
# curr_data = pd.read_csv(file)
# file2 = open('./patriots_win2.csv', 'rb')
# curr_data2 = pd.read_csv(file2)

# curr_titles = curr_data["Title"].to_list()
# curr_titles.append(curr_data2["Title"].to_list())

browser = webdriver.Safari()
browser.get(URL)
# scroll to bottom of top posts, get em all
for i in range(20):
    browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(3)

# parse html into BeautifulSoup object
homepageSoup = BeautifulSoup(browser.page_source, "html.parser")

# get a list of all posts
posts = homepageSoup.find_all("div", class_="post mobile_guest")
links = []
for post in posts:
    body = post.find("div", class_="body")
    top = body.find("div", class_="top")
    link = top.find("a", class_="title")
    links.append(link)

def extract_comments(webpage, link):
    comments = []
    deadass_url = "https://patriots.win" + link
    browser.get(deadass_url)
    # for i in range(10):
    #     button = browser.find_element(By.CLASS_NAME, "view-more-parent-comments")
    #     browser.execute_script("arguments[0].click()", button)
    #     time.sleep(3)
    content = BeautifulSoup(browser.page_source, "html.parser")
    all_comments = content.find_all("div", class_="details") ## edited here to get
    for comment in all_comments:
        comment_proper = comment.find("div", "author") ## edit made here, replace 'content' with 'author' so we can collect usernames
        comments.append(comment_proper.getAttribute('data-author').text)
    return comments

def extract_authors(webpage, link):
    deadass_url = "https://patriots.win" + link
    browser.get(deadass_url)
    content = BeautifulSoup(browser.page_source, "html.parser")
    return set([item.get_attribute("data-author") for item in browser.find_elements_by_css_selector("div[data-author]")])

# posts_dict = {"Title": [],
#             "Post URL": [],
#             "Post Comments": []
#             }

authors = set()

# code commented out for author collection
for link in links:
    authors = authors.union(extract_authors(browser, link["href"]))
    # if link.text in curr_titles:
    #     continue
    # posts_dict["Title"].append(link.text)
    # posts_dict["Post URL"].append(link["href"])
    # comments = extract_comments(browser, link["href"])
    # tot_comments += len(comments)
    # print(tot_comments)
    # posts_dict["Post Comments"].append(comments)

# top_posts = pd.DataFrame(authors)

foo = pd.DataFrame(authors)
name = 'patriots_win_users.csv'
foo.to_csv(name, index=True)

# print(tot_comments)

# name = 'patriots_win_ALLTIME' + '.csv'
# top_posts.to_csv(name, index=True)
