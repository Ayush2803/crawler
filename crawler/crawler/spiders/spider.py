import scrapy
from ..items import CrawlerItem


class msfSpider(scrapy.Spider):
    name = "msfSpider"
    start_urls = [
        "https://www.msf.gov.sg/Pages/default.aspx"
    ]

#---------------------------------------------------------------------------------------#
##################### HELPER FUNCTIONS TO HELP IN CRAWLING###############################
#---------------------------------------------------------------------------------------#

    def parse_all_text(self, response):
        item = CrawlerItem()
        item['headings'] = response.css('h2::text').extract()
        item['headings'].append(response.css('h1::text').extract())
        item['paras'] = response.css('p::text').extract()
        item['paras'].append(response.css('li::text').extract())
        yield item

    def parse_page(self, response):
        item = CrawlerItem()
        content = response.css('.content')
        item['headings'] = response.css('.contentWithSide h1::text').extract()
        item['paras'] = content.css('p::text').extract()
        item['paras'].append(content.css('h2::text').extract())
        item['paras'].append(content.css('h3::text').extract())
        item['paras'].append(content.css('h4::text').extract())
        item['paras'].append(content.css('h5::text').extract())
        item['paras'].append(content.css('ol li::text').extract())
        item['paras'].append(content.css('ul li::text').extract())
        yield item

    def parse_category(self, response):

        page_list = response.css('.listing a::attr(href)').extract()
        for Url in page_list:
            yield response.follow(Url, callback=self.parse_page)

        item = CrawlerItem()
        content = response.css('.content')
        item['headings'] = response.css('.contentWithSide h1::text').extract()
        item['paras'] = content.css('p::text').extract()
        item['paras'].append(content.css('h2::text').extract())
        item['paras'].append(content.css('h3::text').extract())
        item['paras'].append(content.css('h4::text').extract())
        item['paras'].append(content.css('h5::text').extract())
        item['paras'].append(content.css('ol li::text').extract())
        item['paras'].append(content.css('ul li::text').extract())

        yield item

    def parse_pagination(self, response):
        # First deal with pagination links
        read_more_links = response.css('.moreLink::attr(href)').extract()
        for Url in read_more_links:
            yield response.follow(Url, callback=self.parse_page)

        # Go to next page
        next_page = response.css('.nextPg::attr(href)').get()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_policies)

#---------------------------------------------------------------------------------------#
##################### FUNCTIONS TO CRAWL PAGES OF MAIN SITE #############################
#---------------------------------------------------------------------------------------#

    def parse_policies(self, response):
        # Read More
        # First deal with pagination links
        read_more_links = response.css('.moreLink::attr(href)').extract()
        for Url in read_more_links:
            yield response.follow(Url, callback=self.parse_page)

        # Go to next page
        next_page = response.css('.nextPg::attr(href)').get()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_policies)

        # Follow the links on the side bar
        sidebar_links = response.css(
            '.show-hide-block a::attr(href)').extract()
        for Url in sidebar_links:
            yield response.follow(Url, callback=self.parse_category)

    def parse_media(self, response):
        sidebar_links = response.css(
            '.show-hide-block a::attr(href)').extract()
        for Url in sidebar_links:
            yield response.follow(Url, callback=self.parse_pagination)

    def parse_events(self, response):
        read_more_links = response.css('.moreLink::attr(href)').extract()
        for Url in read_more_links:
            yield response.follow(Url, callback=self.parse_page)
            tabs = response.css('.ui-tabs-anchor::attr(href)').extract()
            for tab in tabs:
                yield response.follow(tab, callback=self.parse_page)

    def parse_about(self, response):
        links = response.css(
            '#ctl00_PlaceHolderMain_UIVersionedContent7_PageDisplayModePanel a::attr(href)').extract()
        print(links)
        for Url in links:
            yield response.follow(Url, callback=self.parse_page)

    def parse_page_2(self, response):
        item = CrawlerItem()
        item['headings'] = response.css('h2::text').extract()
        item['paras'] = response.css(
            '#ctl00_PlaceHolderMain_ctl01__ControlWrapper_RichHtmlField span::text').extract()
        yield item

    def parse_side_menu(self, response):
        links = response.css(
            '.sidebar-wrapper-subsubmenu-links a::attr(href)').extract()
        for Url in links:
            yield response.follow(Url, callback=self.parse_page_2)

    def parse_read_more(self, response):
        next_page = response.css(
            '#ctl00_PlaceHolderMain_ctl00__ControlWrapper_RichHtmlField a::attr(href)').extract_first()
        yield response.follow(next_page, callback=self.parse_side_menu)

    def parse_article(self, response):
        item = CrawlerItem()
        item['headings'] = response.css('h2::text').extract()
        item['paras'] = response.css('.ed p::text').extract()
        yield item

    def parse_articles_page(self, response):
        article_links = response.css(
            '.articleItemDesc a::attr(href)').extract()
        for Url in article_links:
            yield response.follow(Url, callback=self.parse_article)

    def parse_parenting(self, response):
        links = response.css('#lifestage-submenu a::attr(href)').extract()
        for Url in links:
            yield response.follow(Url, callback=self.parse_read_more)

        # Articles Page
        next_page = 'https://familiesforlife.sg/discover-an-article/Pages/default.aspx'
        yield response.follow(next_page, self.parse_articles_page)

#---------------------------------------------------------------------------------------#
##################### FUNCTIONS TO CRAWL CHILDREN SITES #################################
#---------------------------------------------------------------------------------------#

    def parse_baby_bonus(self, response):
        item = CrawlerItem()
        contents = response.css('.content-thumbnail-copy')
        for content in contents:
            item['headings'] = content.css('a h4::text').extract()
            item['paras'] = content.css('p::text').extract()

        about_page = 'https://www.babybonus.msf.gov.sg/parent/web/about'
        yield response.follow(about_page, callback=self.parse_all_text)

        parenting_page = 'https://familiesforlife.sg/Parenting/Pages/Home.aspx'
        yield response.follow(parenting_page, callback=self.parse_parenting)

        yield item

    def parse_break_the_silence(self, response):
        item = CrawlerItem()
        item['headings'] = response.css('.main-content-title::text').extract()
        item['paras'] = response.css('.main-article::text').extract()

        menu_links = response.css('.dropdown-submenu a::attr(href)').extract()
        for Url in menu_links:
            yield response.follow(Url, callback=self.parse_all_text)

        yield item

    def parse_comcare_1(self, response):
        item = CrawlerItem()
        item['paras'] = response.css(
            '#ctl00_PlaceHolderMain_UIVersionedContent7_PageDisplayModePanel p::text').extract()
        item['headings'] = response.css('.ms-rteElement-H1::text').extract()
        item['headings'].append(response.css(
            '.ms-rteElement-H2::text').extract())
        yield item

    def parse_comcare_2(self, response):
        sidebar_links = response.css('.sideNav a::attr(href)').extract()
        for Url in sidebar_links:
            yield response.follow(Url, callback=self.parse_comcare_1)

    def parse_divorce(self, response):
        item = CrawlerItem()
        item['paras'] = response.css('.divorceRightText div::text').extract()
        item['paras'].append(response.css(
            '.divorceRightText li::text').extract())
        item['headings'] = response.css('.divorceLeftnav a::text').extract()
        yield item

    def parse_divorce_readmore(self, response):
        links = response.css('.btn::attr(href)').extract()
        for Url in links:
            yield response.follow(Url, callback=self.parse_divorce)

    def parse_ecda_page(self, response):
        item = CrawlerItem()
        item['paras'] = response.css(
            '#ctl00_PlaceHolderMain_PageContent__ControlWrapper_RichHtmlField p::text').extract()
        item['headings'] = response.css(
            '.breadcrumbCurrentNode::text').extract()
        yield item

    def parse_ecda(self, response):
        item = CrawlerItem()
        item['paras'] = response.css('#Content p::text').extract()
        item['headings'] = response.css('h3::text').extract()
        yield item

    def parse_ecda_service(self, response):
        links = response.css('.nostyle a::attr(href)').extract()
        for Url in links:
            yield response.follow(Url, callback=self.parse_ecda_page)

    def parse_ecda_news(self, response):
        links = response.css('#NewsBody a::attr(href)').extract()
        for Url in links:
            yield response.follow(Url, callback=self.parse_ecda_page)

    def parse_enabling(self, response):
        item = CrawlerItem()
        item['paras'] = response.css(
            '#ctl00_PlaceHolderMain_UIVersionedContent7_PageDisplayModePanel p::text').extract()
        item['headings'] = response.css('h1::text').extract()

        yield item

    def parse_family_assist_page(self, response):
        item = CrawlerItem()
        item['paras'] = response.css('#cc-component-1 p::text').extract()
        item['headings'] = response.css('h2::text').extract()

        yield item

    def parse_family_assist(self, response):
        links = response.css(
            '.pdsp-homepage-article-copy-view-more a::attr(href)').extract()
        for Url in links:
            yield response.follow(Url, callback=self.parse_family_assist_page)

    def parse_gpl(self, response):
        item = CrawlerItem()
        item['paras'] = response.css(
            '.MVjpL4v0Q3e0JJXRSlKi2 div div ._1aUEFW0yJvEH_sCcWltAl1 p::text').extract()
        item['headings'] = response.css('h2::text').extract()
        yield item

    def parse_msfcare_about(self, response):
        item = CrawlerItem()
        item['paras'] = response.css('#body-wrapper p::text').extract()
        item['headings'] = response.css('.we-care__title::text').extract()
        item['headings'].append(response.css(
            '.image-text-detail__title::text').extract())
        yield item

    def parse_msfcare_programs(self, response):
        links = response.css('.card a::attr(href)').extract()
        for Url in links:
            yield response.follow(Url, callback=self.parse_msfcare_about)

    def parse_msfcare_stories(self, response):
        item = CrawlerItem()
        item['paras'] = response.css('.js-story-desc::text').extract()
        item['headings'] = response.css('.story__name::text').extract()
        yield item

    def parse_msfcare(self, response):
        item = CrawlerItem()
        item['paras'] = response.css('.masthead__text::text').extract()
        item['paras'].append(response.css('.image-text__text::text').extract())
        item['paras'].append(response.css('.carousel__text::text').extract())
        item['headings'] = response.css('.masthead__title::text').extract()

        about_page = 'https://www.msf.gov.sg/Volunteer/Pages/about-us.aspx'
        yield response.follow(about_page, callback=self.parse_msfcare_about)
        programs_page = 'https://www.msf.gov.sg/Volunteer/Pages/programme-finder.aspx'
        yield response.follow(about_page, callback=self.parse_msfcare_programs)
        stories_page = 'https://www.msf.gov.sg/Volunteer/Pages/stories.aspx'
        yield response.follow(about_page, callback=self.parse_msfcare_stories)

        yield item

    def parse_opg_page(self, response):
        item = CrawlerItem()
        item['paras'] = response.css('#WebPartWPQ2 p::text').extract()
        item['paras'].append(response.css('#WebPartWPQ2 li::text').extract())
        item['headings'] = response.css('.ms-rteForeColor-10::text').extract()
        yield item

    def parse_opg(self, response):
        links = response.css('.main-menu__items a::attr(href)').extract()
        for Url in links:
            yield response.follow(Url, callback=self.parse_opg_page)

#---------------------------------------------------------------------------------------#
##################### THE MAIN PARSE FUNCTION WHICH RUNS FIRST###########################
#---------------------------------------------------------------------------------------#

    def parse(self, response):
        # Parse the home page
        items = CrawlerItem()
        items['headings'] = response.css('h3::text').extract()
        items['paras'] = response.css('.synopsis p::text').extract()

        # Follow to all links in the navbar

        # Policies
        next_page = 'https://www.msf.gov.sg/policies/Pages/default.aspx'
        yield response.follow(next_page, callback=self.parse_policies)

        # Media Rooms
        next_page = 'https://www.msf.gov.sg/media-room/Pages/default.aspx'
        yield response.follow(next_page, callback=self.parse_pagination)
        yield response.follow(next_page, callback=self.parse_media)

        # Assistance
        next_page = 'https://www.msf.gov.sg/assistance/Pages/default.aspx'
        yield response.follow(next_page, callback=self.parse_pagination)
        yield response.follow(next_page, callback=self.parse_media)

        # Events
        next_page = 'https://www.msf.gov.sg/Events/Pages/default.aspx'
        yield response.follow(next_page, callback=self.parse_events)

        # About
        next_page = 'https://www.msf.gov.sg/about-MSF/Pages/default.aspx'
        yield response.follow(next_page, callback=self.parse_about)

        #-------------------------------------------------------------------------------#
        ##################### CRAWL FAMILY OF WEBSITES ##################################
        #-------------------------------------------------------------------------------#

        # 1. Baby Bonus
        next_page = 'https://www.babybonus.msf.gov.sg/parent/web/home'
        yield response.follow(next_page, callback=self.parse_baby_bonus)

        # 2. Break The Silence
        next_page = 'https://www.msf.gov.sg/breakthesilence/pages/home.aspx'
        yield response.follow(next_page, callback=self.parse_break_the_silence)

        # 3. Celebrating Singapore sg women
        next_page = 'https://www.msf.gov.sg/celebrating-sg-women/Pages/default.aspx'
        yield response.follow(next_page, callback=self.parse_all_text)

        # 4. ComCare
        # i) Learn more page
        next_page = 'https://www.msf.gov.sg/Comcare/Pages/Learn-More-About-ComCare.aspx'
        yield response.follow(next_page, callback=self.parse_comcare_1)

        # ii) Assistance page
        next_page = 'https://www.msf.gov.sg/Comcare/Pages/Public-Assistance.aspx'
        yield response.follow(next_page, callback=self.parse_comcare_2)

        # 5. Divorce support
        links_read_more = ['https://www.msf.gov.sg/divorce-support/Pages/default.aspx', 'https://www.msf.gov.sg/divorce-support/Divorce-and-Children/Pages/default.aspx',
                           'https://www.msf.gov.sg/divorce-support/Divorce-Support/Pages/default.aspx', 'https://www.msf.gov.sg/divorce-support/Resources/Pages/default.aspx']
        links_direct = ['https://www.msf.gov.sg/divorce-support/Pages/Online-Counselling.aspx',
                        'https://www.msf.gov.sg/divorce-support/Pages/Mandatory-Parenting-Programme.aspx']

        for Url in links_direct:
            yield response.follow(Url, callback=self.parse_divorce)

        for Url in links_read_more:
            yield response.follow(Url, callback=self.parse_divorce_readmore)

        # 6. Early Childhood Development Agency
        about_page = 'https://www.ecda.gov.sg/pages/aboutus.aspx'
        yield response.follow(about_page, callback=self.parse_ecda)

        services_page = 'https://www.ecda.gov.sg/pages/ourservices.aspx'
        yield response.follow(services_page, callback=self.parse_ecda_service)

        pages = ["{}={}".format(
            "https://www.ecda.gov.sg/pressreleases/pages/default.aspx?Page", str(i)) for i in range(1, 26)]
        for news_page in pages:
            yield response.follow(news_page, callback=self.parse_ecda_news)

        # 7. Enabling Masterplan
        next_links = ['https://www.msf.gov.sg/policies/Disabilities-and-Special-Needs/Enabling-Masterplans/Pages/Introduction.aspx',
                      'https://www.msf.gov.sg/policies/Disabilities-and-Special-Needs/Enabling-Masterplans/Pages/default.aspx', 'msf.gov.sg/policies/Disabilities-and-Special-Needs/Pages/SG-Enable.aspx']
        for Url in next_links:
            yield response.follow(Url, callback=self.parse_enabling)

        # 8. Family Assist
        next_page = 'https://familyassist.msf.gov.sg/'
        yield response.follow(next_page, callback=self.parse_family_assist)

        # 9. Govt paid leave
        next_page = 'https://www.profamilyleave.msf.gov.sg/'
        yield response.follow(next_page, callback=self.parse_gpl)

        # 10. MSF care network
        next_page = 'https://www.msf.gov.sg/volunteer/Pages/home.aspx'
        yield response.follow(next_page, callback=self.parse_msfcare)

        # 11. The Office of the Public Guardian
        next_page = 'https://www.msf.gov.sg/opg/Pages/Home.aspx'
        yield response.follow(next_page, callback=self.parse_opg)

        # 12. Strengthening Families
        url_list = ['https://www.msf.gov.sg/FAMatFSC/Pages/Strengthening-Families-Programme.aspx', 'https://www.msf.gov.sg/FAMatFSC/Pages/Marriage-Support.aspx',
                    'https://www.msf.gov.sg/FAMatFSC/Pages/Divorce-Support.aspx', 'https://www.msf.gov.sg/FAMatFSC/Pages/Family-Counselling.aspx', 'https://www.msf.gov.sg/FAMatFSC/Pages/Related-Services.aspx']
        for Url in url_list:
            yield response.follow(Url, self.parse_enabling)

        yield items
