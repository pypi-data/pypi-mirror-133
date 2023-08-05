import pendulum as time
# from rich.console import Console
from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys

# con = Console()
browser = webdriver.Firefox()
browser.get(
    'https://docs.google.com/forms/d/e/1FAIpQLSelK158XqvduabI2Nb2ODpDoy53QckjYWoaTCrK5MyqG6-s2g/viewform')

now = time.now()

data = {
    'email': 'arsnocturnaaudio@gmail.com',
    'name': 'Robert Mullis',
    'month': now.month,
    'day': now.day,
    'year': now.year,
    'hour': now.hour,
    'minute': now.minute
}


def main():
    ##################################################
    # Email Address
    ##################################################
    email = browser.find_element(By.XPATH, x.email)
    email.send_keys(data['email'])

    ##########################################
    # Name Select
    ###########################################
    name_select = browser.find_element(By.XPATH, x.name_select)
    name_select.click()
    name = browser.find_element(By.XPATH, x.name)
    name.click()

    ###########################################
    # Date XXX
    ###########################################
    month = browser.find_element(By.XPATH, x.month)
    day = browser.find_element(By.XPATH, x.day)
    year = browser.find_element(By.XPATH, x.year)

    month.send_keys(data['month'])
    day.send_keys(data['day'])
    year.send_keys(data['year'])

    ##################################################
    # Time
    #
    # TODO:
    #       - Fix AM/PM
    ##################################################
    hour = browser.find_element(By.XPATH, x.hour)
    minute = browser.find_element(By.XPATH, x.minute)
    # ampm_select = browser.find_element(By.XPATH, x.ampm_select)

    hour.send_keys(data['hour'] % 12)
    minute.send_keys(data['minute'])
    # ampm_select.click()

    # if data['hour'] == data['hour'] % 12:
    # ampm = browser.find_element(By.XPATH, x.am)
    # else:
    # ampm = browser.find_element(By.XPATH, x.pm)

    # ampm.click()

    ###########################################
    # Options
    ###########################################
    no_issues = browser.find_element(By.XPATH, x.no_issues)
    team_finished = browser.find_element(By.XPATH, x.team_finished)
    minutes_early = browser.find_element(By.XPATH, x.minutes_early)

    no_issues.click()
    team_finished.click()
    minutes_early.click()

    ###########################################
    # Paid Time
    ###########################################
    paid_time = browser.find_element(By.XPATH, x.paid_time)
    paid_time.send_keys('60')

    if __package__ is None or __package__ == '':
        import xpaths as x
    else:
        from . import xpaths as x

    main()
