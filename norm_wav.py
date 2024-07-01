import os
import glob
import soundfile as sf
import pyloudnorm as pyln

wav_dir = 'wavs24k'
wav_list = sorted(glob.glob(os.path.join(wav_dir,'*.wav')))

out_dir = 'wavs24k_norm'
os.makedirs(out_dir, exist_ok=True)

for wav_path in wav_list:
	data, rate = sf.read(wav_path) # load audio (with shape (samples, channels))
	# change this according to the sample rate of your audio
	assert rate==24000
	meter = pyln.Meter(rate) # create BS.1770 meter
	loudness = meter.integrated_loudness(data) # measure loudness
	print(loudness)
	# loudness normalize audio to -22 dB LUFS , you can change this value according to your need
	loudness_normalized_audio = pyln.normalize.loudness(data, loudness, -22.0)
	assert len(data)==len(loudness_normalized_audio)
	out_path = os.path.join(out_dir, os.path.basename(wav_path))
	sf.write(out_path, loudness_normalized_audio, rate, 'PCM_16')
