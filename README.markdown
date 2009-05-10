Language detector
==============================

This is just another implementation of the language detector using n-grams. I
also wrote a [PHP Native version](http://github.com/crodas/phplibtextcat/) (in
fact just a wrapper to an existed library). 

Webservice 
-----------------
I created a webservice hosted on the Google AppEngine in a free account, you
might use it however you wish. The app. itself is pretty easy to use, in fact 
it is just an URL with a `text` parameter via GET.

http://textlang.appspot.com/service?text=TEXT_TO_CAT

The application returns an JSON object with the language(s) that it detected.
In case of error it will return an error attribute.

In other to get better results, you might send text with a length between 50
and 2000 letters.
