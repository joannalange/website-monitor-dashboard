REQUIREMENTS = {
    # up and meets the requirements (ncr stands for 'no country redirect' to
    # make sure it's the english website and not local)
    "http://google.com/ncr": ["Maps", "YouTube"],
    # up but only meets one of the requirements
    "http://google.com/": ["YouTube", "These are not the droids you're looking for"],
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
