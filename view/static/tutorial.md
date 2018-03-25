Web Overdrive is a Python Crawler with GUI. You can crawl data with a browser.


### Need to know
Before that you should learn how to view html of a page and `CSS Selector`.


### Example
First of all you need a token. [Contact Me](http://telegram.me/RSoraM)


Choose a site such as [scrapy's blog](https://blog.scrapinghub.com)
![scrapy's blog](https://raw.githubusercontent.com/RSoraM/Storage/master/scrapy's%20blog.png)


I want:
1. Article's Title
2. Article's Date

And I find each Article's Title is in an `a` tag which's parents is a `h2` tag with `.entry-title` class.

![css selector of title](https://raw.githubusercontent.com/RSoraM/Storage/master/css%20selector%20of%20title.png)

So the CSS Selector of Article's Title is `h2.entry-title a`. 

Same as Article's Title. I can get the CSS Selector of Article's Date is `time`.

For this example, you can find the older articles hyperlinks at the bottom of the page. And the CSS Selector is `div.prev-post > a`.

![css selector of next](https://raw.githubusercontent.com/RSoraM/Storage/master/css%20selector%20of%20next.png)

Add Spider
![add spider](https://raw.githubusercontent.com/RSoraM/Storage/master/add%20spider.png)

If I want Title's link, I just need to edit `attr` in the Form.