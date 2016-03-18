import sys
import time
import urllib2
import json

api_key = "mf48qzp5ndaxae7jgtsh6etm"
def URLRequest(url):
    try:
        response = urllib2.urlopen(url)
        #print response.read()
    except urllib2.HTTPError, e:
        print "Error retrieving results"
        print e.code
        print e.reason
        sys.exit()

    return response.read()

def walmartSearch(product):

    print "Recommendations for " + product + ":"

    query_string = "http://api.walmartlabs.com/v1/search?apiKey=" + api_key + "&query=" + product
    response_string = URLRequest(query_string)


    search_data = json.loads(response_string)
    numItems = search_data["numItems"]
    #check that there are results in te search
    if (numItems == 0):
        print "No search results"
        sys.exit()

    return search_data["items"][0]["itemId"]


def walmartRecommendations(itemId):
    query_string = "http://api.walmartlabs.com/v1/nbp?apiKey=" + api_key + "&itemId=" + str(itemId)
    response_string = URLRequest(query_string)
    recommendations = json.loads(response_string)
    return recommendations

def walmartReview(itemId):
    query_string = "http://api.walmartlabs.com/v1/reviews/" + str(itemId) + "?apiKey=" + api_key
    response = URLRequest(query_string)

    review = json.loads(response)
    statistics = review.get("reviewStatistics", {})
    #return 0 rating if the statistics aren't there (happened in testing)
    average = statistics.get("averageOverallRating", 0.0)
    return average

def sortWalmartReviews(recommendations):
    review_dict = {}

    for item in recommendations:
        rating = walmartReview(item["itemId"])
        time.sleep(1)
        review_dict[item["name"]] = rating

    sorted_list = sorted(review_dict, key=review_dict.__getitem__)
    return sorted_list[:-11:-1]

def main():
    itemId =  walmartSearch(sys.argv[1])
    recs = walmartRecommendations(itemId)
    sorted_recs = sortWalmartReviews(recs)
    for x in sorted_recs:
        print x

if __name__ == "__main__": main()
