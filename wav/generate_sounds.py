import numpy as np
import wave
import os

sample_rate = 44100
gain = 1.0

def create_directories():
    """创建音色目录"""
    base_dir = os.path.dirname(__file__)
    for timbre in ['sine', 'triangle', 'square', 'piano', 'music_box', 'pipe_organ']:
        dir_path = os.path.join(base_dir, timbre)
        os.makedirs(dir_path, exist_ok=True)

def save_wav(timbre, filename, waveform):
    """保存wav文件到对应音色目录"""
    audio = (waveform * 32767 * gain).astype(np.int16)
    filepath = os.path.join(os.path.dirname(__file__), timbre, filename)
    with wave.open(filepath, 'w') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(sample_rate)
        f.writeframes(audio.tobytes())
    print(f'{timbre}/{filename} 生成完成')

def generate_sine_tone(freq, duration, sample_rate):
    """正弦波音色"""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    return np.sin(2 * np.pi * freq * t)

def generate_triangle_tone(freq, duration, sample_rate):
    """三角波音色 - 直接生成"""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    phase = (2 * np.pi * freq * t) % (2 * np.pi)
    waveform = 2 / np.pi * np.arcsin(np.sin(phase))
    return waveform

def generate_square_tone(freq, duration, sample_rate):
    """方波音色 - 直接生成"""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    phase = 2 * np.pi * freq * t
    waveform = np.sign(np.sin(phase))
    return waveform

def generate_piano_tone(freq, duration, sample_rate):
    """钢琴音色 - 增强版，真实非谐波公式"""
    t = np.linspace(0, duration, int(sample_rate * duration), False)

    # 非谐波系数 B（钢琴通常在 0.0002-0.0008）
    B = 0.0005

    # 生成25个泛音，使用真实的非谐波公式
    # fn = f0 × n × √(1 + B × n²)
    partials = []
    for n in range(1, 26):  # 1到25个泛音
        # 真实的非谐波频率公式
        inharmonic_factor = np.sqrt(1 + B * (n ** 2))
        actual_freq = freq * n * inharmonic_factor

        # 泛音强度（钢琴低频泛音强，高频弱）
        if n == 1:
            strength = 1.0
        elif n <= 3:
            strength = 0.7 / (n ** 0.5)
        elif n <= 8:
            strength = 0.5 / (n ** 0.7)
        else:
            strength = 0.3 / (n ** 0.9)

        # 分层衰减：低频慢，高频快
        decay_rate = 3.0 + n * 0.8
        partials.append((actual_freq, strength, decay_rate))

    # 生成泛音
    waveform = np.zeros_like(t)
    for actual_freq, strength, decay_rate in partials:
        partial_wave = np.sin(2 * np.pi * actual_freq * t)
        partial_decay = np.exp(-t * decay_rate)
        waveform += strength * partial_wave * partial_decay

    # 复杂的包络：基于真实钢琴测量
    # Attack: 极快起音（2-3ms）
    attack = np.minimum(t * 350, 1.0)

    # 初始冲击瞬态（击弦瞬间）
    initial_transient = np.exp(-t * 40) * 0.4

    # 主要衰减
    main_decay = np.exp(-t * 4.5) * 0.6

    envelope = attack * (initial_transient + main_decay)

    # 噪声层（模拟击弦机械噪声）
    noise = np.random.randn(len(t)) * 0.015
    noise_envelope = np.exp(-t * 80)
    waveform += noise * noise_envelope

    # 琴弦共振（低频）
    resonance = np.sin(2 * np.pi * freq * 0.5 * t) * 0.1 * np.exp(-t * 2.5)
    waveform += resonance

    # 高频亮度（2-4kHz区域）
    brightness_freq = 2500
    brightness = np.sin(2 * np.pi * brightness_freq * t) * 0.03 * np.exp(-t * 15)
    waveform += brightness

    result = waveform * envelope
    return result / np.max(np.abs(result))

def generate_music_box_tone(freq, duration, sample_rate):
    """八音盒音色 - 增强版，金属梳齿物理模型"""
    t = np.linspace(0, duration, int(sample_rate * duration), False)

    # 基频（金属梳齿主振动）
    waveform = np.sin(2 * np.pi * freq * t)

    # 金属梳齿的非谐波（模拟真实金属振动的复杂性）
    # 使用非整数倍的高频
    metallic_partials = [
        (freq * 2.01, 0.08),   # 略微失谐的2倍频
        (freq * 3.02, 0.05),   # 略微失谐的3倍频
        (freq * 4.03, 0.04),   # 略微失谐的4倍频
        (freq * 7.97, 0.06),   # 接近8倍频但略低
        (freq * 11.1, 0.05),   # 高频金属音
        (freq * 15.3, 0.03),   # 超高频金属音
        (freq * 19.7, 0.02),   # 极高频金属泛音
    ]

    metallic = np.zeros_like(t)
    for metallic_freq, strength in metallic_partials:
        # 高频快速衰减
        decay = np.exp(-t * (20 + metallic_freq / freq * 2))
        metallic += strength * np.sin(2 * np.pi * metallic_freq * t) * decay

    waveform += metallic

    # 包络：模拟金属梳齿被拨动
    attack = np.minimum(t * 250, 1.0)  # 极快起音

    # 初始拨动冲击
    pluck = np.exp(-t * 15) * 0.3

    # 持续振动（金属梳齿振动衰减较慢）
    sustain = np.exp(-t * 2.8) * 0.7 + 0.3

    envelope = attack * (pluck + sustain)

    # 金属碰撞噪声（针拨动梳齿的瞬间）
    click_noise = np.random.randn(len(t)) * 0.008
    click_envelope = np.exp(-t * 100)
    waveform += click_noise * click_envelope

    result = waveform * envelope
    return result / np.max(np.abs(result))

def generate_pipe_organ_tone(freq, duration, sample_rate):
    """管风琴音色 - 增强版，丰富谐波持续音"""
    t = np.linspace(0, duration, int(sample_rate * duration), False)

    # 管风琴丰富谐波列（20个谐波）
    harmonics = []
    for n in range(1, 21):
        if n == 1:
            strength = 1.0
        elif n <= 4:
            strength = 0.8 / (n ** 0.5)
        elif n <= 10:
            strength = 0.6 / (n ** 0.6)
        else:
            strength = 0.4 / (n ** 0.8)
        harmonics.append((n, strength))

    # 生成谐波
    waveform = np.zeros_like(t)
    for n, strength in harmonics:
        harmonic_freq = freq * n
        # 高频衰减稍快，但整体衰减都很慢
        decay = np.exp(-t * (1.5 + n * 0.05))
        waveform += strength * np.sin(2 * np.pi * harmonic_freq * t) * decay

    # 包络：缓慢起音，持续稳定
    attack = np.minimum(t * 5, 1.0)  # 较慢起音

    # 极其缓慢的衰减（持续音）
    sustain = np.exp(-t * 1.2) * 0.3 + 0.7

    envelope = attack * sustain

    # 添加空气感噪声（管风琴的风声）
    air_noise = np.random.randn(len(t)) * 0.006
    air_envelope = np.exp(-t * 3) * 0.3 + 0.7
    waveform += air_noise * air_envelope

    result = waveform * envelope
    return result / np.max(np.abs(result))

def apply_fade(waveform, sample_rate, fade_duration=0.02):
    """淡入淡出"""
    fade_samples = int(sample_rate * fade_duration)
    if len(waveform) < fade_samples * 2:
        return waveform
    fade_in = np.linspace(0, 1, fade_samples)
    fade_out = np.linspace(1, 0, fade_samples)
    waveform[:fade_samples] *= fade_in
    waveform[-fade_samples:] *= fade_out
    return waveform

def generate_melodies(tone_generator, timbre_name):
    """生成三种旋律"""

    # 1. task_complete - 上升音阶（渐进式节奏）
    notes = [392, 493, 587, 784]
    durations = [0.15, 0.15, 0.2, 0.5]
    gaps = [0.08, 0.08, 0.08, 0]

    waveform_parts = []
    for i, (freq, dur) in enumerate(zip(notes, durations)):
        tone = tone_generator(freq, dur, sample_rate)
        tone = apply_fade(tone, sample_rate, 0.015)
        waveform_parts.append(tone)
        if i < len(gaps):
            waveform_parts.append(np.zeros(int(sample_rate * gaps[i])))

    waveform_parts.append(np.zeros(int(sample_rate * 0.1)))
    task_complete = np.concatenate(waveform_parts)
    save_wav(timbre_name, 'task_complete.wav', task_complete)

    # 2. attention - 三连音
    note1 = tone_generator(587, 0.08, sample_rate)
    note1 = apply_fade(note1, sample_rate, 0.01)
    gap1 = np.zeros(int(sample_rate * 0.08))
    note2 = tone_generator(587, 0.08, sample_rate)
    note2 = apply_fade(note2, sample_rate, 0.01)
    gap2 = np.zeros(int(sample_rate * 0.08))
    note3 = tone_generator(587, 0.08, sample_rate)
    note3 = apply_fade(note3, sample_rate, 0.01)

    attention = np.concatenate([note1, gap1, note2, gap2, note3, np.zeros(int(sample_rate * 0.1))])
    save_wav(timbre_name, 'attention.wav', attention)

    # 3. error - 双音下降
    note1 = tone_generator(600, 0.2, sample_rate)
    note1 = apply_fade(note1, sample_rate, 0.015)
    note2 = tone_generator(300, 0.35, sample_rate)
    note2 = apply_fade(note2, sample_rate, 0.02)

    error = np.concatenate([note1, note2, np.zeros(int(sample_rate * 0.1))])
    save_wav(timbre_name, 'error.wav', error)

if __name__ == '__main__':
    create_directories()

    print('生成正弦波音色...')
    generate_melodies(generate_sine_tone, 'sine')

    print('\n生成三角波音色...')
    generate_melodies(generate_triangle_tone, 'triangle')

    print('\n生成方波音色...')
    generate_melodies(generate_square_tone, 'square')

    print('\n生成钢琴音色（增强版 - 25个真实非谐波泛音）...')
    generate_melodies(generate_piano_tone, 'piano')

    print('\n生成八音盒音色（增强版 - 金属梳齿物理模型）...')
    generate_melodies(generate_music_box_tone, 'music_box')

    print('\n生成管风琴音色（增强版 - 20个丰富谐波）...')
    generate_melodies(generate_pipe_organ_tone, 'pipe_organ')

    print('\n所有音效生成完成！')
    print('增强内容：')
    print('  钢琴    - 25个泛音，真实非谐波公式 fn=f0*n*sqrt(1+B*n^2)')
    print('  八音盒  - 7个非谐波金属音，模拟梳齿振动')
    print('  管风琴  - 20个谐波，持续稳定，带风声')
