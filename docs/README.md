# Welcome to Astro-ph for Alexa Flash Briefing

![Astro-ph Logo](../Images/Logo128.png)

This is a simple project to allow you to *listen* to your favorite arXiv category on Amazon Echo device. This is done by using the "Flash Briefing" function on Alexa.

There are a few components for this to work:

1. On AWS Lambda, a python script converts the RSS feeds from arXiv into a JSON file that is readable by Alexa.
2. The python script itself is a Flask application. This is because we need to apply Alexa Flash Briefing with a web link to the custom-formated JSON file.
3. Because we are using the simple Flash Briefing instead of Alexa Skill Kits, basically we are not able to change the following:
    - the number of articles to be read
    - the category
    - many others things...

This page is [https://wingkitlee0.github.io/alexa_astroph/](https://wingkitlee0.github.io/alexa_astroph/)


## Guide to Setup..

1. We choose `AWS Lambda` to host and run our python script (Flask app) for conversion. So we will first need to setup a way to upload and deploy a Flask app to AWS. This can be done using `zappa`.

2. After the whole setup process with `zappa`, there should be a link for the lambda function, like this
[https://atawkf2zyd.execute-api.us-east-1.amazonaws.com/dev](https://atawkf2zyd.execute-api.us-east-1.amazonaws.com/dev). The output is basically some json document that satisfies the Alexa Flash Briefing [format](https://developer.amazon.com/docs/flashbriefing/flash-briefing-skill-api-feed-reference.html).

3. Then we can use this link for the Alexa skill.

## Links

- [New Alexa Tutorial: Deploy Flask-Ask Skills to AWS Lambda with Zappa](https://developer.amazon.com/blogs/post/8e8ad73a-99e9-4c0f-a7b3-60f92287b0bf/New-Alexa-Tutorial-Deploy-Flask-Ask-Skills-to-AWS-Lambda-with-Zappa)


