REQUIREMENTS = {
    # up and meets the requirements (ncr stands for 'no country redirect')
    "http://google.com/ncr": ["Google Search", "Feeling Lucky"],
    # up but only meets one of the requirements
    "http://google.com/ncr": ["Google Search", "These are not the droids you're looking for"],
    # site up but the requirements are not met
    "http://google.com/": ["It's a kind of magic"],
    # this will give a 404
    "http://google.com/blabla": ["dummy"],
    # site down
    "http://goooogle.com/": ["dummy"],
}

# determines how often wbesites are being checked, value in seconds, only
# integers allowed
SAMPLE_PERIOD = 10
