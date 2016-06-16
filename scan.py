from requests import Session

# based on https://github.com/cjyoung/MouseBitesWPF/blob/master/MouseBitesWPF/Libraries/HtmlHelper.cs
# from https://stackoverflow.com/questions/33746440/python-requests-post-failing-with-500-error & https://stackoverflow.com/questions/33696631/sending-post-through-requests-with-cookies-and-authentication
def check_for_reservation(search_date, search_time):
    url = "https://disneyworld.disney.go.com/dining/magic-kingdom/cinderella-royal-table/"
    url2 = "https://disneyworld.disney.go.com/finder/dining-availability"
    session = Session()

    tokenRequest = session.get(url)#, headers=header)
    start = tokenRequest.content.find('''id="pep_csrf"''')
    pep = tokenRequest.content[start+21:tokenRequest.content.find('>',start+22)-1]

    raw = "&searchDate="+str(search_date)+"&skipPricing=true&searchTime="+str(search_time)+"&partySize=6&id=90002464%3BentityType%3Drestaurant&type=dining&pep_csrf=" + pep

    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US, en;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Referer': url,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

    result = session.post(url2, data=raw, headers=headers)

    if result.status_code == 200:
        return result, True
    else:
        return result, False

if __name__ == "__main__":
    dates = ['2016-06-26', '2016-06-27', '2016-06-28', '2016-06-29', '2016-06-30', '2016-07-01']
    meals = {80000712: 'breakfast', 80000717: 'lunch', 80000714: 'dinner'}
    times = [80000712, 80000717, 80000714]
    for date in dates:
        for time in times:
            result, success = check_for_reservation(date, time)
            if not success:
                raise ValueError('Status Code is %s' % result.status_code)
            if 'notAvailable' in result.content:
                print '%s - %s: not available' % (date, meals[time])
            else:
                print '%s - %s: AVAILABLE!!!' % (date, meals[time])
                print result.content
