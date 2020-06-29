def test_landing_page(driver, live_server):
    driver.get(live_server.url)
    # Find an input element
    assert driver.find_element_by_css_selector('input.user-guess')
    assert driver.find_element_by_css_selector('.submit-btn')
    assert driver.find_element_by_css_selector('.user-label')
    assert driver.find_element_by_css_selector('.min-num-lab')
    assert driver.find_element_by_css_selector('.max-num-lab')


def test_guess_random_number(driver, live_server, user_selects_between_1_and_10, user_send_keys):
    user_send_keys('5')
    response_message = driver.find_element_by_css_selector('.response-message')
    response_message = response_message.text
    assert 'success' in response_message.lower() or \
        'sorry' in response_message.lower()


def test_try_again(driver, live_server, user_selects_between_1_and_10, user_send_keys):
    user_send_keys('5')
    # Find the try again button
    try_again_button = driver.find_element_by_css_selector('.try-again')
    try_again_button.click()
    # Check inputs again
    assert driver.find_element_by_css_selector('.user-label')


def test_limits(driver, live_server, user_selects_between_1_and_10, user_send_keys):
    user_send_keys('123')
    response_message = driver.find_element_by_css_selector('.response-message')
    assert 'choose another number' in response_message.text.lower()


def test_empty_vals(driver, live_server):
    driver.get(live_server.url)
    submit_button = driver.find_element_by_css_selector('.submit-btn')
    submit_button.click()
    response_message = driver.find_element_by_css_selector('.response-message')
    assert 'missing inputs' in response_message.text.lower()


def test_style(driver, live_server):
    driver.get(live_server.url)
    nav_bar = driver.find_element_by_css_selector('.nav-bar')
    assert 'mb-3' in nav_bar.get_attribute('class')
