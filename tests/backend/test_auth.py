def test_initial_state(auth):
    assert auth.can_attempt_login
    assert not auth.is_authenticated
    assert auth.remaining_attempts == 3

def test_is_authenticated_after_correct_password(auth):
    """
    Tests that the system is unlocked after entering the correct password.
    """
    auth.login('1234')
    assert auth.is_authenticated

def test_is_not_authenticated_after_incorrect_password(auth):
    """
    Tests that the system stays locked after entering an incorrect pin.
    """
    auth.login('0000')
    assert not auth.is_authenticated

def test_can_attempt_after_incorrect_password(auth):
    """
    Tests that the user can re-try entering a PIN after a signle incorrect attempt.
    """
    auth.login('0000')
    assert auth.can_attempt_login

def test_can_login_after_failed_attempt(auth):
    """
    Tests that the user can login with the correct PIN after an unsuccessful attempt.
    """
    auth.login('0000')
    assert not auth.is_authenticated

    auth.login('1234')
    assert auth.is_authenticated

def test_remaining_attemps_decrease_after_incorrect_password(auth):
    """
    Tests that the number of attempts increases after entering an incorrect password.
    """
    auth.login('0000')
    assert auth.remaining_attempts == 2

def test_cannot_attempt_after_three_incorrect_attempts(auth):
    """
    Tests that the user cannot re-try logging in immediately after three incorrect attempts.
    """
    auth.login('0000')
    auth.login('0000')
    auth.login('0000')
    assert not auth.can_attempt_login

def test_state_restored_after_thirty_second_timeout(auth, qtbot):
    """
    Tests that the Auth class resets back to initial state after the 30-second timeout.
    """
    auth.login('0000')
    auth.login('0000')
    auth.login('0000')

    qtbot.wait(30 * 1000)
    assert auth.can_attempt_login
    assert not auth.is_authenticated
    assert auth.remaining_attempts == 3

def test_can_login_after_thirty_second_timeout(auth, qtbot):
    """
    Tests that the user can login with the correct PIN after awaiting the 30-second timeout (from three failed attempts).
    """
    auth.login('0000')
    auth.login('0000')
    auth.login('0000')

    qtbot.wait(30 * 1000)
    
    auth.login('1234')
    assert auth.is_authenticated

def test_state_restored_after_logout(auth):
    """
    Tests that the system Auth class resets back to initial state after logging out.
    """
    auth.login('1234')
    auth.logout()

    assert auth.can_attempt_login
    assert not auth.is_authenticated
    assert auth.remaining_attempts == 3