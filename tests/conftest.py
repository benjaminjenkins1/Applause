import pytest

from applause.model import *

import datetime

@pytest.fixture(scope='module')
def new_user():
  user=User(email    ='testuser@test.com',
            pass_hash='testpasswordhash',
            activated=False,
            banned   =False)
  return user

@pytest.fixture(scope='module')
def new_domain():
  domain=Domain(did        =123,
                domain_name='example.com',
                email      ='testuser@test.com',
                validated  =False)
  return domain

@pytest.fixture(scope='module')
def new_key():
  key=Key(uuid ='fe9eb8f0-8d65-4915-82ef-8085e42bd586',
          did  =123,
          email='testuser@test.com')
  return key

@pytest.fixture(scope='module')
def new_page():
  page=Page(pid =234,
            did =123,
            path='/a/page')
  return page

@pytest.fixture(scope='module')
def new_clap():
  clap=Clap(pid      =234,
            ip       ='192.168.1.35',
            num_claps=5)
  return clap

@pytest.fixture(scope='module')
def new_page_view():
  page_view=PageView(pvid=345,
                     pid=234,
                     ip='192.168.1.35',
                     referrer='google.com',
                     start_time=datetime.datetime(2000,1,1),
                     time_on_page=datetime.timedelta(seconds=60))
  return page_view