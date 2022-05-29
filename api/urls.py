from django.urls import path

from api.views.WordList import WordList
from api.views.mango_views import Mangos, MangoDetail
from api.views.poem_views import PoemDetail, Poems, PublicPoems
from api.views.user_views import SignUp, SignIn, SignOut, ChangePassword
from api.views.word_views import Words, WordDetail, PublicWords

urlpatterns = [
  # Restful routing
  path('mangos/', Mangos.as_view(), name='mangos'),
  path('mangos/<int:pk>/', MangoDetail.as_view(), name='mango_detail'),

  path('poems/', Poems.as_view(), name='poems'),
  path('poems/<int:pk>/', PoemDetail.as_view(), name='poem_detail'),
  path('poems/<int:pk>/words/', Words.as_view(), name='poem_detail'),
  path('poems/<int:pk>/words/<int:sk>/', WordDetail.as_view(), name='word_detail'),
  path('wordlist/', WordList.as_view(), name='wordlist'),

  path('publicpoems/', PublicPoems.as_view(), name='publicpoems'),
  path('publicwords/', PublicWords.as_view(), name='publicwords'),

  path('sign-up/', SignUp.as_view(), name='sign-up'),
  path('sign-in/', SignIn.as_view(), name='sign-in'),
  path('sign-out/', SignOut.as_view(), name='sign-out'),
  path('change-pw/', ChangePassword.as_view(), name='change-pw')
]
