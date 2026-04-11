# ======================
# Play Sound Behavior
# ======================

def test_play_sets_current_sound(sound_player, sound_mid_volume):
    sound_player.play(sound_mid_volume)
    assert sound_mid_volume in sound_player.current_sounds

def test_play_sets_current_volume(sound_player, sound_mid_volume):
    sound_player.play(sound_mid_volume)
    assert sound_player.current_volume == sound_mid_volume.volume

def test_play_returns_filename_in_result(sound_player, sound_mid_volume):
    result = sound_player.play(sound_mid_volume)
    assert "test.wav" in result[1]

# ======================
# Stop Sound Behavior
# ======================

def test_stop_clears_current_sounds(sound_player, sound_mid_volume):
    sound_player.play(sound_mid_volume)
    sound_player.stop()
    assert sound_player.current_sounds == []

def test_stop_with_no_current_sound(sound_player):
    result = sound_player.stop()
    assert result == "Stopped all sounds"

# ======================
# Increment Sound Behavior
# ======================

def test_incr_volume_increases_volume(sound_player, sound_low_volume):
    sound_player.play(sound_low_volume)
    before = sound_player.current_volume
    sound_player.incr_volume()
    assert sound_player.current_volume > before

def test_incr_volume_does_not_exceed_max(sound_player, sound_mid_volume):
    sound_player.play(sound_mid_volume)
    sound_player.current_volume = 100
    sound_player.incr_volume()
    assert sound_player.current_volume == 100

def test_incr_volume_no_sound_playing(sound_player, monkeypatch):
    monkeypatch.setattr("pygame.mixer.get_busy", lambda: False)
    result = sound_player.incr_volume()
    assert result == "No sound is currently playing"

# ======================
# Decrement Sound Behavior
# ======================

def test_decr_volume_decreases_volume(sound_player, sound_mid_volume):
    sound_player.play(sound_mid_volume)
    before = sound_player.current_volume
    sound_player.decr_volume()
    assert sound_player.current_volume < before

def test_decr_volume_does_not_go_below_min(sound_player, sound_mid_volume):
    sound_player.play(sound_mid_volume)
    sound_player.current_volume = 0
    sound_player.decr_volume()
    assert sound_player.current_volume == 0

def test_decr_volume_no_sound_playing(sound_player, monkeypatch):
    monkeypatch.setattr("pygame.mixer.get_busy", lambda: False)
    result = sound_player.decr_volume()
    assert result == "No sound is currently playing"

# ======================
# Error Handling
# ======================

def test_play_returns_error_on_failure(sound_player, sound_mid_volume, monkeypatch):
    monkeypatch.setattr("pygame.mixer.Sound", lambda f: (_ for _ in ()).throw(FileNotFoundError("test.wav")))
    result = sound_player.play(sound_mid_volume)
    assert result[0] == False
    assert "Failed to play sound" in result[1]

def test_play_does_not_add_to_current_sounds_on_failure(sound_player, sound_mid_volume, monkeypatch):
    monkeypatch.setattr("pygame.mixer.Sound", lambda f: (_ for _ in ()).throw(FileNotFoundError("test.wav")))
    sound_player.play(sound_mid_volume)
    assert sound_player.current_sounds == []

def test_stop_returns_success(sound_player):
    result = sound_player.stop()
    assert result == "Stopped all sounds"

def test_incr_volume_returns_string_on_success(sound_player, sound_mid_volume):
    sound_player.play(sound_mid_volume)
    result = sound_player.incr_volume()
    assert "volume" in result.lower()

def test_decr_volume_returns_string_on_success(sound_player, sound_mid_volume):
    sound_player.play(sound_mid_volume)
    result = sound_player.decr_volume()
    assert "volume" in result.lower()