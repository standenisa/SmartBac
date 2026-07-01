import { TextStyle } from 'react-native';
import { DUO } from './duo';

export const TYPO: Record<string, TextStyle> = {
  heading1: { fontSize: 28, fontFamily: DUO.fontBlack, letterSpacing: -0.5 },
  heading2: { fontSize: 22, fontFamily: DUO.fontExtraBold, letterSpacing: -0.3 },
  heading3: { fontSize: 18, fontFamily: DUO.fontBold, letterSpacing: -0.2 },
  subheading: { fontSize: 16, fontFamily: DUO.fontSemiBold, letterSpacing: -0.1 },
  label: { fontSize: 13, fontFamily: DUO.fontSemiBold },
  body: { fontSize: 15, fontFamily: DUO.fontMedium, lineHeight: 22 },
  caption: { fontSize: 11, fontFamily: DUO.fontBold, letterSpacing: 1, textTransform: 'uppercase' },
  math: { fontSize: 16, fontFamily: 'monospace' },
  button: { fontSize: 16, fontFamily: DUO.fontExtraBold, letterSpacing: 0.5, textTransform: 'uppercase' },
  badge: { fontSize: 12, fontFamily: DUO.fontBold },
  stat: { fontSize: 22, fontFamily: DUO.fontExtraBold },
};
