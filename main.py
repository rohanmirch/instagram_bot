# Instagram bot
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from passwords import USER, PW, FRIENDS


class insta_bot:
    def __init__(self, username, pw):
        self.username = username
        self.pw = pw
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        #self.driver = webdriver.Chrome()
        self.driver.get("https://www.instagram.com/")
        self.driver.implicitly_wait(3)

        # Log in
        self.driver.find_element_by_xpath("//input[@name='username']").send_keys(username)
        self.driver.find_element_by_xpath("//input[@name='password']").send_keys(pw)
        self.driver.find_element_by_xpath("//button[@type='submit']").click()
        #time.sleep(4)
        self.driver.implicitly_wait(4)

        # Close popups
        self.driver.find_element_by_xpath("//button[text()='Not Now']").click()
        self.driver.implicitly_wait(4)

        self.driver.find_element_by_xpath("//button[contains(text(),'Not Now')]").click()
        self.driver.implicitly_wait(3)

        # Go to user's home page
        self.driver.find_element_by_xpath("//a[contains(@href, '/{}')]".format(self.username)).click()
        time.sleep(2)

        # Get followers and following profiles
        #self.followers = self.get_followers()
        #self.following = self.get_following()


    def get_followers(self):
        ''' From a user's page, get profles that follow the user.'''
        #self.driver.find_element_by_xpath("//a[contains(@href, '/{}')]".format(self.username)).click()
        #time.sleep(3)
        if self.driver.current_url != "https://www.instagram.com/{}/".format(USER):
            self.driver.get("https://www.instagram.com/{}/".format(USER))
            self.driver.implicitly_wait(2.5)

        self.driver.find_element_by_xpath("//a[contains(@href, '/followers')]").click()
        time.sleep(1.5)
        
        # Scroll to bottom of scroll box, then keep scrolling 
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div[2]")
        prev, curr = 0, 1
        while prev != curr:
            prev = curr
            # Execute javascript (scroll_box = arguments[0])
            curr = self.driver.execute_script(
                ''' arguments[0].scrollTo(0, arguments[0].scrollHeight);
                    return arguments[0].scrollHeight;
                ''', scroll_box)
            time.sleep(1.5)

        # Get all followers and remove blank empty strings
        links = scroll_box.find_elements_by_tag_name("a")
        followers = [link.text for link in links if link.text != ""]      

        #Close tab
        self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div[1]/div/div[2]/button").click()

        return followers


    def get_following(self):
        ''' From a user's page, get profiles that the user is following. '''

        if self.driver.current_url != "https://www.instagram.com/{}/".format(USER):
            self.driver.get("https://www.instagram.com/{}/".format(USER))
            self.driver.implicitly_wait(2.5)

        self.driver.find_element_by_xpath("//a[contains(@href, '/following')]").click()
        time.sleep(1.5)
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div[2]")
        prev, curr = 0, 1
        while prev != curr:
            prev = curr
            # Execute javascript (scroll_box = arguments[0])
            curr = self.driver.execute_script(
                ''' arguments[0].scrollTo(0, arguments[0].scrollHeight);
                    return arguments[0].scrollHeight;
                ''', scroll_box)
            time.sleep(1.5)
        links = scroll_box.find_elements_by_tag_name("a")
        following = [link.text for link in links if link.text != ""]
        
        #Close tab
        self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div[1]/div/div[2]/button").click()
        time.sleep(1)

        return following

    def send_message(self, to_users, message):
        ''' Sends direct message to multiple to_users (list) or single to_users (str). '''
        if type(to_users) == str:
            to_users = [to_users]

        for to_user in to_users:
            self.driver.get("https://www.instagram.com/direct/inbox")
            self.driver.implicitly_wait(2)

            #self.driver.find_element_by_xpath("//*[@id="react-root"]/section/div/div[2]/div/div/div[1]/div[1]/div/div[3]/button").click()
            self.driver.find_element_by_xpath("//button[contains(text(),'Send Message')]").click()
            self.driver.implicitly_wait(1)
            # Type user into search
            self.driver.find_element_by_xpath("//input[@name='queryBox']").send_keys(to_user)
            self.driver.implicitly_wait(3)
            # Click user button (should be at the top of list)
            #self.driver.find_element_by_xpath("//div[contains(text(),'{}')]".format(to_user)).click()

            #self.driver.find_element_by_xpath("//img[contains(@alt, '{}')]".format(to_user)).click()
            #elem = self.driver.find_element_by_xpath("//div[text()='{}']".format(to_user))
            #print(elem.text)
            #elem.click()
            self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div[2]/div[2]/div[1]/div/div[3]/button").click()
            

            # Click next
            self.driver.find_element_by_xpath("//div[text()='Next']").click()
            self.driver.implicitly_wait(2)

            # Send message
            text_area = self.driver.find_element_by_tag_name("textarea")
            text_area.send_keys(message)
            self.driver.find_element_by_xpath("//button[contains(text(),'Send')]").click()
            time.sleep(1)



    # Ideas:
    # For a gieven account, get similar accounts: /user/similar_accounts
    #   - can then follow, message, or just compile

i = insta_bot(USER, PW)

to_users = FRIENDS
message = "test"
i.send_message(to_users, message)
i.get_followers()
#i.get_following()
