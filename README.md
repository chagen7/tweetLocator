# tweetLocator
This program displays a map showing locations of Twitter tweets matching user-specific search terms.

This program:
  - has a GUI that enables the user to enter a location and search terms
  - queries Twitter to gather tweets based on the search terms and the location
  - displays a static map with markers showing the locations of the tweets returned by the search. For tweets that don't have specific geocode information, there is only a pin for that tweet in the center of the map. The marker for the currently displayed tweet looks different than markers for the other tweets.
  - displays the number of tweets retrieved
  - displays details of a "current" tweet and provides a way to "step through" each of the retrieved tweets:
      - to step through tweets, you could provide, for example, "Next Tweet" and "Previous Tweet" buttons.
  - for the current tweet, displays at least the tweet text, the screen name, and name of the user who created the tweet.
  - for the current tweet, also provides a way to open a browser and display the web page corresponding to URLs embedded in the tweets.


Important enabling steps:

  - need a twitter Developer account with "Elevated" access so that you can use Twitter API v1.1.
  - obtain API keys (to add to twitteraccess.py).
  - able to import some tools to enable proper connection to Twitter using the Oauth secure authorization protocol.
