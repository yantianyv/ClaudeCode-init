import numpy as np
import wave
import os

sample_rate = 44100
gain = 1.0  # 最大音量

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
    # 直接三角波公式
    waveform = 2 / np.pi * np.arcsin(np.sin(phase))
    return waveform

def generate_square_tone(freq, duration, sample_rate):
    """方波音色 - 直接生成"""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    phase = 2 * np.pi * freq * t
    # 直接方波公式
    waveform = np.sign(np.sin(phase))
    return waveform

def generate_piano_tone(freq, duration, sample_rate):
    """钢琴音色 - 加法合成，强调非谐波和瞬态"""
    t = np.linspace(0, duration, int(sample_rate * duration), False)

    # 钢琴泛音列（含非谐波）
    partials = [
        (1.0, 1.0, 4.0),       # 基频，慢衰减
        (2.0, 0.65, 5.0),      # 2倍频，稍快
        (3.0, 0.45, 6.0),      # 3倍频
        (4.0, 0.35, 7.0),      # 4倍频
        (5.0, 0.25, 8.0),      # 5倍频
        (6.0, 0.18, 9.0),      # 6倍频
        (7.98, 0.12, 10.0),    # 非谐波！这是关键
        (9.0, 0.08, 12.0),     # 9倍频
        (12.0, 0.05, 15.0),    # 12倍频
    ]
    waveform = np.zeros_like(t)

    for partial_ratio, strength, decay_rate in partials:
        partial_freq = freq * partial_ratio
        # 每个泛音独立衰减
        partial_decay = np.exp(-t * decay_rate)
        waveform += strength * np.sin(2 * np.pi * partial_freq * t) * partial_decay

    # 包络：极快起音 + 初始峰值 + 指数衰减
    attack = np.minimum(t * 150, 1.0)  # 5ms内起音
    initial_peak = np.exp(-t * 30) * 0.35  # 击弦冲击
    decay = np.exp(-t * 4.0) * 0.65  # 主要衰减
    envelope = attack * (initial_peak + decay)

    # 击弦噪声（瞬态）
    noise = np.random.randn(len(t)) * 0.012
    noise_envelope = np.exp(-t * 60)
    waveform += noise * noise_envelope

    # 低频共振（琴身共鸣）
    resonance = np.sin(2 * np.pi * freq * 0.5 * t) * 0.08 * np.exp(-t * 3)
    waveform += resonance

    result = waveform * envelope
    return result / np.max(np.abs(result))

def generate_music_box_tone(freq, duration, sample_rate):
    """八音盒音色 - 纯净基频 + 金属撞击高频"""
    t = np.linspace(0, duration, int(sample_rate * duration), False)

    # 基频（纯净正弦波）
    waveform = np.sin(2 * np.pi * freq * t)

    # 金属撞击高频（非谐波，快速衰减）
    metallic_freqs = [freq * 9, freq * 13, freq * 17]
    metallic = np.zeros_like(t)
    for mf in metallic_freqs:
        # 高频也用正弦波，但快速衰减
        metallic += np.sin(2 * np.pi * mf * t) * 0.05

    metallic_envelope = np.exp(-t * 18)
    waveform += metallic * metallic_envelope

    # 包络：瞬间起音 + 持续音
    attack = np.minimum(t * 200, 1.0)
    pluck = np.exp(-t * 10) * 0.25  # 拨动感
    sustain = np.exp(-t * 2.5) * 0.75 + 0.25
    envelope = attack * (pluck + sustain)

    result = waveform * envelope
    return result / np.max(np.abs(result))

def generate_pipe_organ_tone(freq, duration, sample_rate):
    """管风琴音色 - 丰富谐波，持续稳定"""
    t = np.linspace(0, duration, int(sample_rate * duration), False)

    # 管风琴丰富谐波列
    partials = [
        (1.0, 1.0),       # 基频
        (2.0, 0.7),       # 2倍频
        (3.0, 0.5),       # 3倍频
        (4.0, 0.4),       # 4倍频
        (5.0, 0.3),       # 5倍频
        (6.0, 0.2),       # 6倍频
        (8.0, 0.15),      # 8倍频
        (10.0, 0.1),      # 10倍频
        (12.0, 0.08),     # 12倍频
    ]
    waveform = np.zeros_like(t)

    for partial_ratio, strength in partials:
        partial_freq = freq * partial_ratio
        waveform += strength * np.sin(2 * np.pi * partial_freq * t)

    # 包络：缓慢起音，持续稳定
    attack = np.minimum(t * 6, 1.0)  # 较慢起音
    sustain = np.exp(-t * 1.5) * 0.4 + 0.6  # 持续音，衰减很慢
    envelope = attack * sustain

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
    # 节奏模式：短-短-中-长，音符之间有间隔
    notes = [392, 493, 587, 784]  # G4→B4→D5→G5，降低一个音区
    durations = [0.15, 0.15, 0.2, 0.5]  # 渐进式增长，最后一个音更长
    gaps = [0.08, 0.08, 0.08, 0]  # 前三个音符后有间隔

    waveform_parts = []
    for i, (freq, dur) in enumerate(zip(notes, durations)):
        tone = tone_generator(freq, dur, sample_rate)
        tone = apply_fade(tone, sample_rate, 0.015)
        waveform_parts.append(tone)
        if i < len(gaps):
            waveform_parts.append(np.zeros(int(sample_rate * gaps[i])))

    # 结尾添加空白
    waveform_parts.append(np.zeros(int(sample_rate * 0.1)))
    task_complete = np.concatenate(waveform_parts)
    save_wav(timbre_name, 'task_complete.wav', task_complete)

    # 2. attention - 三连音（三个短促音）
    note1 = tone_generator(587, 0.08, sample_rate)  # D5，降低音调
    note1 = apply_fade(note1, sample_rate, 0.01)
    gap1 = np.zeros(int(sample_rate * 0.08))
    note2 = tone_generator(587, 0.08, sample_rate)  # D5
    note2 = apply_fade(note2, sample_rate, 0.01)
    gap2 = np.zeros(int(sample_rate * 0.08))
    note3 = tone_generator(587, 0.08, sample_rate)  # D5
    note3 = apply_fade(note3, sample_rate, 0.01)

    attention = np.concatenate([note1, gap1, note2, gap2, note3, np.zeros(int(sample_rate * 0.1))])
    save_wav(timbre_name, 'attention.wav', attention)

    # 3. error - 双音下降（连续无间隔）
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

    print('\n生成钢琴音色...')
    generate_melodies(generate_piano_tone, 'piano')

    print('\n生成八音盒音色...')
    generate_melodies(generate_music_box_tone, 'music_box')

    print('\n生成管风琴音色...')
    generate_melodies(generate_pipe_organ_tone, 'pipe_organ')

    print('\n所有音效生成完成！')
    print('目录结构：')
    print('  sine/       - 正弦波音色（纯电子音）')
    print('  triangle/   - 三角波音色（明亮柔和）')
    print('  square/     - 方波音色（8-bit游戏感）')
    print('  piano/      - 钢琴音色（醇厚有弹性）')
    print('  music_box/  - 八音盒音色（金属簧片打击感）')
    print('  pipe_organ/ - 管风琴音色（持续稳定）')
