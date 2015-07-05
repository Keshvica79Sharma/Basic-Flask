from app import app
import unittest


class Flask_test_cases(unittest.TestCase):
  
# Ensure the index page is rendered properly
  def test_01_index_page_loads_correctly(self):
    tester = app.test_client(self)
    response = tester.get('/')
    self.assertEqual(200,response.status_code)
    self.assertIn('This is the index page',response.data)

# Ensure the welcome page loads correctly and asks for login
  def test_02_welcome_page_loads_correctly(self):
    tester = app.test_client(self)
    response = tester.get('/welcome')
    self.assertEqual(200,response.status_code)
    self.assertIn('Please login to enter',response.data)

# Ensure the login route loads correctly
  def test_03_login_page_loads_correctly(self):
    tester = app.test_client(self)
    response = tester.get('/login')
    self.assertEqual(200,response.status_code)
    self.assertIn('Please login',response.data)

# Login page behaves correctly with incorrect credentials
  def test_04_login_page_behaves_correctly_with_incorrect_credentials(self):
    tester = app.test_client(self)
    response = tester.post('/login',data={"mobile":"0000000000","otp":"1111"})
    self.assertIn('Invalid credentials. Please try again.',response.data)

# Login page behaves correctly with correct credentials
  def test_05_login_page_behaves_correctly_with_correct_credentials(self):
    tester = app.test_client(self)
    response = tester.post('/login',data={"mobile":"9999999999","otp":"9999"},follow_redirects=True) # IMPORTANT ::: To follow the redirect to dashboard
    self.assertIn('You have been logged in',response.data)

# Esure that upon login the data is retrieved from the database
  def test_06_upon_login_the_data_is_retrieved(self):
    tester = app.test_client(self)
    response = tester.post('/login', data={"mobile":"7777777777","otp":"2222"}, follow_redirects=True)
    self.assertIn('Awsome blog',response.data)

# Ensure that you cannot access the dashboard route before login
  def test_07_the_dashboard_cannot_be_accessed_withot_login(self):
    tester = app.test_client(self)
    response = tester.get('/dashboard',follow_redirects=True)
    self.assertIn('You need to login first',response.data)
    
if __name__ == '__main__' :
  unittest.main()
