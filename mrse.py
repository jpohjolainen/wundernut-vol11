#!/usr/bin/env python3
##
#
# Morse code decipher from wav files.
#
# Doesn't require any 3rd party libraries.
#
# Save this file to filename 'morse_decode.py' and in give execute permissions.
# (in linux/macosx: chmod 0755 morse_decode.py)
#
# usage: ./morse_decode.py <wav-file>
#
# (c) Janne Pohjolainen 2022
#
import sys
import math
import wave
import struct

MORSE={
    ".-": "A",
    "-...": "B",
    "-.-.": "C",
    "-..": "D",
    ".": "E",
    "..-.": "F",
    "--.": "G",
    "....": "H",
    "..": "I",
    ".---": "J",
    "-.-": "K",
    ".-..": "L",
    "--": "M",
    "-.": "N",
    "---": "O",
    ".--.": "P",
    "--.-": "Q",
    ".-.": "R",
    "...": "S",
    "-": "T",
    "..-": "U",
    "...-": "V",
    ".--": "W",
    "-..-": "X",
    "-.--": "Y",
    "--..": "Z",
    ".-.-.-": "."
}

RMS_THRESHOLD = 0.100

def rms(block, bits):
    count = len(block) / 2
    sum_squares = 0.0
    for sample in block:
        n = sample * (1.0 / (pow(2, bits) / 2))
        sum_squares += n*n
    return math.sqrt(sum_squares / count)

def main():
    if len(sys.argv) < 2:
        print(f"usage: morse_decode.py <wav-file>")
        sys.exit(1)

    wavefile = wave.open(sys.argv[1])
    wavemeta = wavefile.getparams()
    bits = wavemeta.sampwidth * 8
    frate = wavemeta.framerate
    nframes = wavemeta.nframes
    blocksize = int(frate * 0.01)

    signal = "00"
    for i in range(0, nframes, blocksize):
        frame = wavefile.readframes(blocksize)
        read = len(frame)
        u = struct.unpack(f"<{int(read / 2)}h", frame)
        r = rms(u, bits)
        if r > RMS_THRESHOLD:
            signal += "1"
        else:
            signal += "0"

    signal = signal.lstrip('0')

    # calculate 0 and 1 lengths
    last = "0"
    li = 0
    f = []
    for i in range(0, len(signal)):
        if signal[i] != last:
            f.append((last, len(signal[li:i])))
            li = i
        last = signal[i]

    # get lengths of all 0s
    m0 = sorted(set([x[1] for x in f if x[0] == '0']))

    # sort and separate 0s into groups which are 2 times the lengths of previous
    # these will be the separators of letters and words
    sep = [m0[i] for i in range(0,len(m0)) if m0[i] > m0[i-1] * 2]

    for word in signal.split('0' * sep[2]):
        letters = word.split('0' * sep[1])
        for let in letters:
            didah = let.split('0' * sep[0])
            letter = ""
            for x in didah:
                x = x.strip('0')
                if len(x) > 9:
                    letter += "-"
                else:
                    if '1' in x:
                        letter += "."
            if letter:
                print(MORSE[letter], end='')
        print(' ', end='')

if __name__ == '__main__':
    main()
