#!/usr/bin/env python
# coding: utf-8

# In[1]:


# !pip install feedparser
# !pip install arrow


# In[2]:


feed_path = 'https://feeds.bbci.co.uk/zhongwen/simp/rss.xml'


# In[3]:


import feedparser
import arrow
import qrcode

feed = feedparser.parse(feed_path)


# In[4]:


def get_info(entry):
    # Thu, 11 Mar 2021 09:45:37 GMT
    date_format = 'ddd, DD MMM YYYY HH:mm:ss ZZZ'
    return entry.title, entry.summary, arrow.get(entry.published, date_format).to('Asia/Shanghai').format('D MMMM YYYY (ZZZ)'), entry.link

def get_info_list(entries, end=10, start=0):
    return [get_info(i) for i in entries[start:end]]

# get_info_list(feed.entries, 1)


# In[5]:


def generate_img(entries, img_idx=0):
    from PIL import Image, ImageDraw, ImageFont
    import textwrap

    logo = Image.open('./bbc_news_cn_logo.png').convert(mode='RGBA')

    def get_font(size=24):
        return ImageFont.truetype("Songti.ttc", size=size)

    def get_qrcode_image(link):
        qr_img = qrcode.make(link)
        
        return qr_img.resize((96, 96))

    def get_wrap_text(text, width=20):
        return textwrap.wrap(text, width=width)

    def draw_entry(draw, offset, entry):
        title, summary, published, link = entry

        title_font = get_font(48)
        title_color = (255, 255, 255)

        summary_font = get_font(36)
        summary_color = (200, 200, 200)

        published_font = get_font(32)
        published_color = (255, 100, 100)
        published_offset = offset[0], offset[1] - 32 - 4
        
        qrcode_img_offset = offset[0] - 128, offset[1]
        qrcode_img = get_qrcode_image(link)

        # Draw Published
        draw.text(published_offset, published, font=published_font, fill=published_color)

        # Draw Title
        draw.text(offset, title, font=title_font, fill=title_color)
        
        # Draw QR Code
        img.paste(qrcode_img, qrcode_img_offset, mask=qrcode_img)

        # Draw Summary
        for idx, line in enumerate(get_wrap_text(summary, width=40)):
            summary_offset = offset[0], offset[1] + 48 + 8 + (idx * 36)
            draw.text(summary_offset, line, font=summary_font, fill=summary_color)

    img_width = 1920
    img_height = 1200
    img = Image.new('RGBA', (img_width, img_height), (0,0,0,255))
    draw = ImageDraw.Draw(img, mode='RGBA')

    top_offset = 200

    for idx, entry in enumerate(entries):
        offset_x = 200
        offset_y = idx * 200 + top_offset
        draw_entry(draw, (offset_x, offset_y), entry)

    img.paste(logo, (200, 0), mask=logo)

    img.save('./bbc_{}.png'.format(img_idx))


# In[6]:


# entries = get_info_list(feed.entries, start=0, end=5)

# generate_img(entries, 0)


# In[7]:


for i in range(1):
    start = i * 5
    end = (i+1) * 5
    entries = get_info_list(feed.entries, start=start, end=end)

    generate_img(entries, i)


# In[ ]:




