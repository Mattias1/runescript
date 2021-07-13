import argparse


class Rune:
    def __init__(self, string):
        s = string.split(maxsplit=3)
        self.rune = s[0]
        self.futhorc = s[1]
        self.name = s[2]

class Runescript:
    def __init__(self):
        self.runes = self.loadRunes()

    def loadRunes(self):
        runes = [
                'ᚠ f  feh',
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
        return map(lambda s: Rune(s), runes)

    def translate(self, text: str, fr: str, to: str):
        lookup = self._buildLookup(fr)
        translation = []
        # TODO: this doesn't work with two letter combinations
        # (aka, -ef 'ng' gives 'ᚾᚷ' rather then 'ᛝ')
        for c in text:
            try:
                if to == 'english':
                    translation.append(lookup[c].futhorc)
                elif to == 'futhorc':
                    translation.append(lookup[c].rune)
            except KeyError:
                translation.append(c)
        return ''.join(translation)

    def _buildLookup(self, fr: str):
        if fr == 'english':
            return { r.futhorc : r for r in self.runes }
        return { r.rune : r for r in self.runes }


def main():
    parser = argparse.ArgumentParser(
            description='A little tool to convert runescript back and forth.')
    parser.add_argument('--version', action='version', version='runescript 1.0')
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

        rs = Runescript()
        translation = rs.translate(text, fr, to)
        print(translation)
    except KeyboardInterrupt:
        print(' Exiting.')


main()
