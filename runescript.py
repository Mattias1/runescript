import argparse


class Rune:
    def __init__(self, rune, futhorc, name):
        self.rune = rune
        self.futhorc = futhorc
        self.name = name

    @classmethod
    def fromString(self, string):
        s = string.split(maxsplit=3)
        return self(s[0], s[1], s[2])


class Runescript:
    def __init__(self):
        self.runes = self.loadRunes()

    def loadRunes(self):
        runeList = [
            'ᚠ f  feh',
            'ᚢ v  ur (*alternative)',
            'ᚢ u  ur',
            'ᚦ th thorn',
            'ᚩ o  os',
            'ᚱ r  rada',
            'ᚳ c  cen',
            'ᚲ k  kaunan (*elder futhark)',
            'ᚷ g  geofu',
            'ᚹ w  wyn',
            'ᚺ h  hagalaz (*elder futhark)',
            'ᚻ h  hægil',
            'ᚾ n  næd',
            'ᛁ i  is',
            'ᛃ j  jēra (*elder futhark)',
            'ᛄ j  gær (*alternative)',
            'ᛡ j  gær',
            'ᛇ ï  ih',
            'ᛈ p  peord',
            'ᛉ x  ilcs',
            'ᛊ s  sōwilō (*elder futhark)',
            'ᚴ s  sygil (*alternative)',
            'ᛋ s  sygil',
            'ᛏ t  ti',
            'ᛒ b  berc',
            'ᛖ e  eh',
            'ᛗ m  mon',
            'ᛚ l  lagu',
            'ᛜ ng ingwaz (*elder futhark)',
            'ᛝ ng ing',
            'ᛟ oe oedil',
            'ᛞ d  dæg',
            'ᚪ a  ac',
            'ᚫ ae æsc',
            'ᛠ ea ear',
            'ᚣ y  yr',
        ]
        runes = list(map(lambda s: Rune.fromString(s), runeList))
        runes.append(Rune('᛫', ' ', 'space'))
        return runes

    def translate(self, text: str, fr: str, to: str):
        lookup = self._buildLookup(fr)
        translation = []
        # TODO: this doesn't work with two letter combinations
        # (aka, -ef 'ng' gives 'ᚾᚷ' rather then 'ᛝ')
        i = 0
        while i < len(text):
            c = text[i]
            try:
                cc = c + text[i + 1]
                result = self._translateChar(lookup, cc, to)
                i += 1
            except (KeyError, IndexError) as e:
                try:
                    result = self._translateChar(lookup, c, to)
                except KeyError:
                    result = c
            translation.append(result)
            i += 1
        return ''.join(translation)

    def _buildLookup(self, fr: str):
        if fr == 'english':
            return {r.futhorc: r for r in self.runes}
        return {r.rune: r for r in self.runes}

    def _translateChar(self, lookup, c: str, to: str):
        if to == 'english':
            return lookup[c].futhorc
        elif to == 'futhorc':
            return lookup[c].rune
        raise ValueError('Unknown script to translate to', to)


def main():
    parser = argparse.ArgumentParser(
        description='A little tool to convert runescript back and forth.')
    parser.add_argument('--version', action='version', version='v1.1')
    parser.add_argument('text', type=str, nargs='*', help='the text to convert')
    parser.add_argument('-ef', action='store_true',
                        help='parse english to futhorc (default)')
    parser.add_argument('-fe', action='store_true',
                        help='parse futhorc to english')
    args = parser.parse_args()

    try:
        (fr, to) = ('english', 'futhorc')
        if args.fe:
            (fr, to) = ('futhorc', 'english')

        if len(args.text) == 0:
            text = input('Enter ' + fr + ' to translate: ')
        else:
            text = ' '.join(args.text)

        if fr == 'english':
            text = text.lower()

        rs = Runescript()
        translation = rs.translate(text, fr, to)
        print(translation)
    except KeyboardInterrupt:
        print(' Exiting.')


main()
