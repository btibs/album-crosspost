# Facebook album code

import requests

LIMIT = 25

class FacebookAlbumIterator:
    """Iterator for listing all of a user's albums"""
    def __init__(self, graph):
        self.graph = graph
        self.response = self.graph.request("me?fields=albums&limit=%s" % LIMIT)['albums']
        self.index = 0
        self.stopped = False

    def __iter__(self):
        return self

    def __next__(self):
        if "data" not in self.response or len(self.response['data']) == 0:
            self.stopped = True
        
        if self.stopped:
            raise StopIteration

        album = self.response['data'][self.index]
        self.index += 1

        if self.index == len(self.response['data']):
            # Load the next page of results
            if "next" in self.response['paging']:
                request_next = self.response['paging']['next']
                self.response = requests.get(request_next).json()
                self.index = 0
            else:
                self.stopped = True

        return album

class FacebookPhotoIterator:
    """Iterator for listing photos in a particular album"""
    def __init__(self, graph, album_id):
        self.graph = graph
        self.album_id = album_id
        self.index = 0
        self.stopped = False
        self.response = self.graph.request(album_id+"/photos?limit=%s" % LIMIT)

    def __iter__(self):
        return self

    def __next__(self):
        if "data" not in self.response or len(self.response['data']) == 0:
            self.stopped = True

        if self.stopped:
            raise StopIteration

        photo = self.response['data'][self.index]
        self.index += 1

        if self.index == len(self.response['data']):
            # Load the next page of results
            if "next" in self.response['paging']:
                request_next = self.response['paging']['next']
                self.response = requests.get(request_next).json()
                self.index = 0
            else:
                self.stopped = True

        return photo
