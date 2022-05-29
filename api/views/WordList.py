from rest_framework import generics
from rest_framework.response import Response

import random


class WordList(generics.ListCreateAPIView):
    def get(self, request):
        """Index request"""
        wordfile = open("docs/wordlist10000.txt", "r")
        wordlist = wordfile.readlines()
        wordfile.close()
        wordlist = (random.choices(wordlist, k=29))
        wordlist = (list(map(str.strip, wordlist)))
        wordlist = wordlist + ['+=+=+=+=+=+=+=+=', 'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'I']

        return Response(wordlist)
