![](https://github.com/BahramJannesar/SpringInstagramBot/blob/master/image/spring_bot.jpg)
## Spring Instagram Bot

A bot for gaining the followers that is related to your business, if you are a makeup artist or you have bakery in your house and want to develope your social media marketing that related to your job, i told you this bot can help you to gain more followers.

### Why "Spring" ?

For the first time i run this Bot for my frinend "Bahar" that her name means "Spring" in persian, she lives in [Isfahan](https://en.wikipedia.org/wiki/Isfahan) and has a small bakery there at her house and wants to raise her follower for making more customers.
her page is available [here](https://www.instagram.com/springcake_isfahan/) , her cakes are very delicious. ( :cake: )

### Dependencies 

I used the [private-instagram-library](https://github.com/ping/instagram_private_api) pakage for this project, this pakage very valuable for using instagram API
for installing these dependencies check that repo.

#### First Step :

For the first step you have three choice:
*  Gain the target user followers ( users that follow target user )
*  Gain the target user likers ( users that like on target user's  post)
*  Gain the target user commenters ( users that take comments on target user's post ) --> commenters is a funny name that i picked for these users ( :laughing: )

For Followers :

        python3 gain_follower.py -u USERNAME -p PASSWORD -t TARGET_USERNAME -o followers -cf NUMBER_OF_FOLLOWERS_YOU_WANT_GAIN

For Likers :

        python3 gain_likers.py -u USERNAME -p PASSWORD -t TARGET_USERNAME -o likers -cl NUMBER_OF_LIKERS_YOU_WANT_GAIN

For Commenters :
 
        python3 gain_commenters.py -u USERNAME -p PASSWORD -t TARGET_USERNAME  -o commenters -cc NUMBER_OF_COMMENTERS_YOU_WANT_GAIN

#### Second Step :

This step of project must run every day at the specific time, every time this scrpit runs, follows 50 account for you this limitaion is just for instagram API request rate limit, i propose to you 08:00 PM, beacuse this time is more efficiently (this is my experience) but in every country this time is different.
for this job i propose to you to run this script on your server with [crontab](https://crontab.guru/), it helps you to run script with time scheduling.

For every choise that you choosed from step one you can run :

    python3 follow_username.py -u USERNAME -p PASSWORD -t TARGET_USERNAME -o { followers , likers , commenters }
    
#### Third Step :

This step has been created for usernames that don't follow you back, i run this script on server 2 times on a week with corntab just like second step.

    python3 unfollow_username.py -u USERNAME -p PASSWORD

### Donate

If this bot helps you to making more customers or develope your social media marketing donate me. 
Thanks a lot ( :thumbsup: )

![btc](https://raw.githubusercontent.com/reek/anti-adblock-killer/gh-pages/images/bitcoin.png) Bitcoin: `1D8hw5MRCaHegNhC4rs8nhet9KT9t9qTVC`
