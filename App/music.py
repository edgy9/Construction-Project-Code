from pydub import AudioSegment
from pydub.playback import play
#import simpleaudio as sa


# pip install simpleaudio
# pip install pydub


# Load your audio files
left_sound = AudioSegment.from_file("sounds\example sound 1.wav")
right_sound = AudioSegment.from_file("sounds\example sound 2.wav")

# Make sure both sounds are mono (one channel)
left_sound = left_sound.set_channels(1)
right_sound = right_sound.set_channels(1)

# Combine the two mono sounds into a stereo sound
stereo_sound = AudioSegment.from_mono_audiosegments(left_sound, right_sound)

# Export the combined stereo sound (optional, if you want to save it)
stereo_sound.export("stereo_output.wav", format="wav")

# Play the stereo sound
play(stereo_sound)

# Alternative playback using simpleaudio (if `play` method causes any issues)
#wave_obj = sa.WaveObject.from_wave_file("stereo_output.wav")
#play_obj = wave_obj.play()
#play_obj.wait_done()  # Wait until sound has finished playing