
import datetime

def test_new_user(new_user):
  assert new_user.email=='testuser@test.com'
  assert new_user.pass_hash=='testpasswordhash'
  assert new_user.activated==False
  assert new_user.banned==False

def test_new_domain(new_domain):
  assert new_domain.did==123
  assert new_domain.domain_name=='example.com'
  assert new_domain.email=='testuser@test.com'
  assert new_domain.validated==False

def test_new_key(new_key):
  assert new_key.uuid=='fe9eb8f0-8d65-4915-82ef-8085e42bd586'
  assert new_key.did==123
  assert new_key.email=='testuser@test.com'

def test_new_page(new_page):
  assert new_page.pid==234
  assert new_page.did==123
  assert new_page.path=='/a/page'
  
def test_new_clap(new_clap):
  assert new_clap.pid==234
  assert new_clap.ip=='192.168.1.35'
  assert new_clap.num_claps==5

def test_new_page_view(new_page_view):
  assert new_page_view.pvid==345
  assert new_page_view.pid==234
  assert new_page_view.ip=='192.168.1.35'
  assert new_page_view.referrer=='google.com'
  assert new_page_view.start_time==datetime.datetime(2000,1,1)
  assert new_page_view.time_on_page==datetime.timedelta(seconds=60)