from requests_html import HTML, HTMLSession
import csv
import re
import time


csv_file = open('reviews2.csv', 'w')
csv_write = csv.writer(csv_file)


def search_items(): #return list of data-asin
    session = HTMLSession()
    print("Search for your product here:")
    url_search = "https://www.amazon.com/s?k="
    search_words = (input()).replace(" ","+")

    
    url = "https://www.amazon.com/s?k={search_words}".format(search_words=search_words)
    r = session.get(url)
    r.html.render(sleep=2)
    data_asin = r.html.find('div[data-asin]')
    lst_data_asin = []
    for item in data_asin:
        asin = item.attrs["data-asin"]
        if asin!='':
            lst_data_asin.append(asin)
    return lst_data_asin


def find_reviews(lst_data_asin, rv_number_pages):
    lst_header = ["Prod. Title", "Prod. Asin"]
    n = rv_number_pages * 10
    for i in range(n):
        string = f"Review {i}"
        lst_header.append(string)
    csv_write.writerow(lst_header)
    print(f"{len(lst_data_asin)} products found!")
    for asin in lst_data_asin:
        search = True
        k = 0
        lst_csv_reviews = []
        print("asin:",asin)
        while (search):
            k+=1
            print("pag:",k)
            
            session = HTMLSession()
            url = f"https://www.amazon.com/product-reviews/{asin}/ref=cm_cr_arp_d_paging_btm_next_2?pageNumber={k}" 
            r = session.get(url)
            r.html.render(sleep=3)
            title = r.html.find('h1.a-size-large.a-text-ellipsis',first=True).text
            
            #lst_csv_reviews = [title, asin]
            #reviews

            reviewSession = r.html.find('div.a-section.a-spacing-none.reviews-content.a-size-base', first=True)
            lst_reviews = reviewSession.find('div.a-section.celwidget')
            #print("lista de rewviews",lst_reviews)


            for review in lst_reviews:
                a_reviewtitle = review.find('a[data-hook="review-title"]',first=True)
                if a_reviewtitle:
                    review_title = a_reviewtitle.text
                    stars = review_title[:3]
                    rv_title = review_title[19:]
                    #print(f"title: {rv_title} stars: {stars}")
                    text = review.find('span[data-hook="review-body"]',first=True).text
                    
                    review_cell = f"Title: {rv_title}\nStars: {stars}\n{text}"

                    #print(review_cell)
                    lst_csv_reviews.append(review_cell)
                else:
                    print("No more reviews")
                    search = False
            
            if k>=rv_number_pages:
                search = False
        lst_csv_reviews.insert(0,title)
        lst_csv_reviews.insert(1,asin)


        print(lst_csv_reviews)
        csv_write.writerow(lst_csv_reviews)
    csv_file.close()




rv_number_pages = 2 #number of review's pages to acess


lst_asin = search_items()

find_reviews(lst_asin, rv_number_pages)







