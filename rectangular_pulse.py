import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.stats import norm

# Parameters
num_bits = 1000          # Number of bits to transmit
M = 4                    # π/4-QPSK is a 4-symbol modulation scheme
SNR_dB = np.arange(0, 15, 2)  # Range of SNR values in dB for BER analysis
bit_rate = 1e3           # Bit rate in bits per second
symbol_rate = bit_rate / 2  # π/4-QPSK: 2 bits per symbol

# Generate random bits
bits = np.random.randint(0, 2, num_bits)

# Map bits to π/4-QPSK symbols
def pi_4_qpsk_modulate(bits):
    # Split bits into pairs
    bits = bits.reshape((-1, 2))
    symbols = np.zeros(len(bits), dtype=complex)
    phase = 0  # Starting phase

    for i, bit_pair in enumerate(bits):
        # Map bit pairs to phase shifts
        if np.array_equal(bit_pair, [0, 0]):
            phase += np.pi / 4
        elif np.array_equal(bit_pair, [0, 1]):
            phase += 3 * np.pi / 4
        elif np.array_equal(bit_pair, [1, 1]):
            phase += 5 * np.pi / 4
        elif np.array_equal(bit_pair, [1, 0]):
            phase += 7 * np.pi / 4
        # Keep phase in range [-π, π]
        phase = np.angle(np.exp(1j * phase))
        symbols[i] = np.exp(1j * phase)
    return symbols

# Modulate the bits
symbols = pi_4_qpsk_modulate(bits)

# Function to add noise
def add_awgn_noise(signal, snr_dB):
    snr_linear = 10 ** (snr_dB / 10.0)
    power_signal = np.mean(np.abs(signal)**2)
    noise_power = power_signal / snr_linear
    noise = np.sqrt(noise_power / 2) * (np.random.randn(*signal.shape) + 1j * np.random.randn(*signal.shape))
    return signal + noise

# Demodulation for π/4-QPSK
def pi_4_qpsk_demodulate(symbols):
    received_bits = []
    prev_phase = 0

    for sym in symbols:
        phase_diff = np.angle(sym) - prev_phase
        prev_phase = np.angle(sym)

        if -np.pi / 4 <= phase_diff < np.pi / 4:
            received_bits.extend([0, 0])
        elif np.pi / 4 <= phase_diff < 3 * np.pi / 4:
            received_bits.extend([0, 1])
        elif -3 * np.pi / 4 <= phase_diff < -np.pi / 4:
            received_bits.extend([1, 0])
        else:
            received_bits.extend([1, 1])

    return np.array(received_bits)

# BER calculation function
def calculate_ber(original_bits, received_bits):
    return np.sum(original_bits != received_bits) / len(original_bits)

# Run simulation over SNR range
ber = []
for snr in SNR_dB:
    noisy_symbols = add_awgn_noise(symbols, snr)
    received_bits = pi_4_qpsk_demodulate(noisy_symbols)
    ber.append(calculate_ber(bits, received_bits[:len(bits)]))

# Plot BER vs. SNR
plt.figure(figsize=(10, 6))
plt.semilogy(SNR_dB, ber, 'o-', label='Simulated BER')
plt.xlabel('SNR (dB)')
plt.ylabel('Bit Error Rate (BER)')
plt.title('BER vs SNR for π/4-QPSK')
plt.grid(True)
plt.legend()
plt.show()

# Plot constellation diagram
plt.figure(figsize=(8, 8))
plt.scatter(noisy_symbols.real, noisy_symbols.imag, color='blue', alpha=0.5, label="Received symbols")
plt.scatter(symbols.real, symbols.imag, color='red', marker='x', label="Transmitted symbols")
plt.xlabel('In-Phase')
plt.ylabel('Quadrature')
plt.title('Constellation Diagram for π/4-QPSK')
plt.legend()
plt.grid(True)
plt.show()

# Eye diagram
def plot_eye_diagram(signal, sps=8):
    plt.figure(figsize=(10, 6))
    num_symbols = len(signal) // sps
    for i in range(num_symbols - 1):
        plt.plot(signal[i * sps:(i + 2) * sps].real, color='blue', alpha=0.5)
    plt.title("Eye Diagram for π/4-QPSK")
    plt.xlabel("Sample")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.show()

# Generate eye diagram with oversampling
oversampled_signal = np.repeat(symbols, 8)  # 8 samples per symbol
noisy_oversampled_signal = add_awgn_noise(oversampled_signal, 10)  # Example SNR
plot_eye_diagram(noisy_oversampled_signal)
