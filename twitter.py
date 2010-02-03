import urllib
import json

class Twitter():
    """Describes a Twitter object."""
    
    url_search = 'http://search.twitter.com/search.json'
    url_trends = 'http://search.twitter.com/trends.json'
    url_user_timeline = 'http://twitter.com/statuses/user_timeline.json'
    url_friends_timeline = 'http://twitter.com/statuses/friends_timeline.json'
    url_public_timeline = 'http://twitter.com/statuses/public_timeline.json'
    url_status_update = 'http://twitter.com/statuses/update.json'
    
    def __init__(self):
        """Sets the page attribute."""
        self.page = 1
        
    def select_action(self):
        """Creates an interface to all Twitter actions defined in this class."""
        action = raw_input('s: search; t: trends; u: user timeline; f: friends timeline; p: public timeline; up: update status: ').strip()
        if 's' == action:
            q = raw_input('Enter search string: ')
            self.get_search(q)
        elif 't' == action:
            self.get_trends()
        elif 'u' == action:
            screen_name = raw_input('Enter screen name: ')
            self.get_user_timeline(screen_name)
        elif 'f' == action:
            self.get_friends_timeline()
        elif 'p' == action:
            self.get_public_timeline()
        elif 'up' == action:
            status = raw_input('Enter status: ')
            self.post_status_update(status)
        else:
            exit('Invalid action')
        
    def get_search(self, q=None):
        """Gets tweets that match a specific query."""
        if not q:
            q = raw_input('Enter search string: ')
        json_obj = self._get_json_obj(self.url_search, {'q': q, 'page': self.page})
        for r in [result['text'] for result in json_obj['results']]:
            print r
        self._set_next_page()
        self.get_search(q)
        
    def get_trends(self):
        """Gets the top ten topics that are currently trending on Twitter."""
        json_obj = self._get_json_obj(self.url_trends)
        for t in [trend['name'] for trend in json_obj['trends']]:
            print t
        
    def get_user_timeline(self, screen_name=None):
        """Gets the 20 most recent statuses posted from the authenticating user."""
        if not screen_name:
            screen_name = raw_input('Enter screen name: ')
        json_obj = self._get_json_obj(self.url_user_timeline, {'screen_name': screen_name, 'page': self.page})
        for s in [status['text'] for status in json_obj]:
            print s
        self._set_next_page()
        self.get_user_timeline(screen_name)
        
    def get_friends_timeline(self):
        """Gets the 20 most recent statuses posted by the authenticating user and that user's friends."""
        json_obj = self._get_json_obj(self.url_friends_timeline, {'page': self.page})
        for s in [(status['user']['screen_name'], status['text']) for status in json_obj]:
            print s[0] + ': ' + s[1]
        self._set_next_page()
        self.get_friends_timeline()
        
    def get_public_timeline(self):
        """Gets the 20 most recent statuses from non-protected users who have set a custom user icon."""
        json_obj = self._get_json_obj(self.url_public_timeline)
        for s in [status['text'] for status in json_obj]:
            print s
        
    def post_status_update(self, status=None):
        """Updates the authenticating user's status."""
        if not status:
            status = raw_input('Enter status: ')
        params = urllib.urlencode({'status': status})
        urllib.urlopen(self.url_status_update, params)
        
    def _get_json_obj(self, url, param_dict={}):
        """Makes API requests and parses the response."""
        params   = urllib.urlencode(param_dict)
        url_obj  = urllib.urlopen('%s?%s' % (url, params))
        json_obj = json.load(url_obj)
        if 'error' in json_obj:
            exit(json_obj['error'])
        return json_obj
    
    def _set_next_page(self):
        """Creates an interface to set the sext page or quit."""
        next_action = raw_input('enter: next page; q: quit: ')
        if 'q' == next_action:
            exit()
        else:
            self.page += 1
            
if __name__ == "__main__":
    Twitter().select_action()