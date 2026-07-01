import { Platform, Text, View, StyleSheet, TextStyle } from 'react-native';
import { DUO } from '@/constants/duo';

// On web, use KaTeX. On native, fall back to sanitized unicode text.
let InlineMath: any = null;
let BlockMath: any = null;
if (Platform.OS === 'web') {
  const rk = require('react-katex');
  InlineMath = rk.InlineMath;
  BlockMath = rk.BlockMath;
  // Inject KaTeX CSS + dark mode override
  if (typeof document !== 'undefined' && !document.getElementById('katex-css')) {
    const link = document.createElement('link');
    link.id = 'katex-css';
    link.rel = 'stylesheet';
    link.href = 'https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css';
    document.head.appendChild(link);
    // Dark theme override
    const style = document.createElement('style');
    style.id = 'katex-dark';
    style.textContent = `
      .katex { color: ${DUO.textPrimary}; font-size: 1.1em; }
      .katex-display { margin: 0.4em 0; }
      .katex-display > .katex { color: ${DUO.textPrimary}; }
      .katex .mord, .katex .mbin, .katex .mrel,
      .katex .mopen, .katex .mclose, .katex .mpunct,
      .katex .minner, .katex .mop { color: inherit; }
      .katex .sqrt > .sqrt-sign { color: ${DUO.textPrimary}; }
      .katex .frac-line { border-bottom-color: ${DUO.textSecondary}; }
      .katex .overline .overline-line, .katex .underline .underline-line { border-bottom-color: ${DUO.textPrimary}; }
    `;
    document.head.appendChild(style);
  }
}

// Unicode super/subscript maps for exponents and indices
const SUPERSCRIPTS: Record<string, string> = {
  '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹',
  '+': '⁺', '-': '⁻', '=': '⁼', '(': '⁽', ')': '⁾', 'n': 'ⁿ', 'i': 'ⁱ', 'x': 'ˣ',
};
const SUBSCRIPTS: Record<string, string> = {
  '0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄', '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉',
  '+': '₊', '-': '₋', '=': '₌', '(': '₍', ')': '₎', 'n': 'ₙ', 'i': 'ᵢ', 'x': 'ₓ',
};

// Map a whole string via a table; returns null if any char is not mappable
function mapAll(d: string, table: Record<string, string>): string | null {
  let out = '';
  for (const c of d) {
    if (c in table) out += table[c];
    else return null;
  }
  return out;
}

// Convert x^2, x**2, x_1 etc. to unicode superscripts/subscripts.
// Keeps the original text when an exponent isn't fully mappable.
function exponentsToUnicode(s: string): string {
  return s
    // a**2 or a**(-2)  -> a²
    .replace(/([A-Za-z0-9)\]])\s*\*\*\s*\(?(-?[0-9]+)\)?/g, (m, b, d) => {
      const r = mapAll(d, SUPERSCRIPTS); return r ? b + r : m;
    })
    // ^{...}
    .replace(/\^\{\s*([^}]+?)\s*\}/g, (m, d) => {
      const r = mapAll(d, SUPERSCRIPTS); return r ?? m;
    })
    // ^2, ^(-2), ^n
    .replace(/\^\(?(-?[0-9A-Za-z]+)\)?/g, (m, d) => {
      const r = mapAll(d, SUPERSCRIPTS); return r ?? m;
    })
    // _{...}
    .replace(/_\{\s*([^}]+?)\s*\}/g, (m, d) => {
      const r = mapAll(d, SUBSCRIPTS); return r ?? m;
    })
    // _1, _n
    .replace(/_\(?([0-9A-Za-z]+)\)?/g, (m, d) => {
      const r = mapAll(d, SUBSCRIPTS); return r ?? m;
    });
}

// Convert common LaTeX commands to readable unicode for native fallback
function latexToUnicode(s: string): string {
  return exponentsToUnicode(s)
    .replace(/\\int\b/g, '∫')
    .replace(/\\sum\b/g, '∑')
    .replace(/\\prod\b/g, '∏')
    .replace(/\\lim\b/g, 'lim')
    .replace(/\\infty\b/g, '∞')
    .replace(/\\pi\b/g, 'π')
    .replace(/\\alpha\b/g, 'α')
    .replace(/\\beta\b/g, 'β')
    .replace(/\\gamma\b/g, 'γ')
    .replace(/\\theta\b/g, 'θ')
    .replace(/\\cdot\b/g, '·')
    .replace(/\\times\b/g, '×')
    .replace(/\\div\b/g, '÷')
    .replace(/\\pm\b/g, '±')
    .replace(/\\leq\b/g, '≤')
    .replace(/\\geq\b/g, '≥')
    .replace(/\\neq\b/g, '≠')
    .replace(/\\sqrt\{([^}]*)\}/g, '√($1)')
    .replace(/\\frac\{([^}]*)\}\{([^}]*)\}/g, '($1)/($2)')
    .replace(/\\left|\\right/g, '')
    .replace(/\\,|\\;|\\!/g, ' ')
    .replace(/\^\{([^}]*)\}/g, '^$1')
    .replace(/_\{([^}]*)\}/g, '_$1')
    .replace(/\\\\/g, ' ')
    .trim();
}

// Split text into alternating plain + math segments
type Segment = { type: 'text' | 'inline' | 'block'; content: string };

function parseSegments(input: string): Segment[] {
  const segments: Segment[] = [];
  const re = /\\\[([\s\S]+?)\\\]|\\\(([\s\S]+?)\\\)|\$\$([\s\S]+?)\$\$|\$([^$\n]+?)\$/g;
  let last = 0;
  let m: RegExpExecArray | null;
  while ((m = re.exec(input)) !== null) {
    if (m.index > last) {
      segments.push({ type: 'text', content: input.slice(last, m.index) });
    }
    if (m[1] !== undefined) segments.push({ type: 'block', content: m[1] });
    else if (m[2] !== undefined) segments.push({ type: 'inline', content: m[2] });
    else if (m[3] !== undefined) segments.push({ type: 'block', content: m[3] });
    else if (m[4] !== undefined) segments.push({ type: 'inline', content: m[4] });
    last = re.lastIndex;
  }
  if (last < input.length) {
    segments.push({ type: 'text', content: input.slice(last) });
  }
  return segments;
}

// Heuristic: if no delimiters but contains LaTeX commands, treat whole thing as inline math
function hasLatexCommands(s: string): boolean {
  return /\\(int|sum|frac|sqrt|lim|infty|pi|alpha|beta|gamma|theta|cdot|times|left|right)\b/.test(s);
}

export interface MathTextProps {
  text: string;
  style?: TextStyle;
  block?: boolean;
}

export default function MathText({ text, style, block }: MathTextProps) {
  if (!text) return null;

  let segments = parseSegments(text);
  if (segments.length === 0 || (segments.length === 1 && segments[0].type === 'text' && hasLatexCommands(text))) {
    segments = [{ type: block ? 'block' : 'inline', content: text }];
  }

  if (Platform.OS === 'web' && InlineMath) {
    return (
      <View style={[styles.webWrap, block && styles.webBlock]}>
        {segments.map((seg, i) => {
          if (seg.type === 'text') {
            return (
              <Text key={i} style={[styles.text, style]}>
                {exponentsToUnicode(seg.content)}
              </Text>
            );
          }
          const Cmp = seg.type === 'block' ? BlockMath : InlineMath;
          return (
            <View key={i} style={seg.type === 'block' ? styles.blockMath : styles.inlineMath}>
              <Cmp math={seg.content.trim()} />
            </View>
          );
        })}
      </View>
    );
  }

  // Native fallback: render as unicode text
  const plain = segments
    .map((seg) => (seg.type === 'text' ? seg.content : latexToUnicode(seg.content)))
    .join('');
  return <Text style={[styles.text, style]}>{plain}</Text>;
}

const styles = StyleSheet.create({
  webWrap: { flexDirection: 'row', flexWrap: 'wrap', alignItems: 'center' },
  webBlock: { flexDirection: 'column', alignItems: 'flex-start' },
  text: { fontSize: 15, color: DUO.textPrimary, lineHeight: 22, fontWeight: '600' },
  inlineMath: { marginHorizontal: 2 },
  blockMath: { marginVertical: 4, alignSelf: 'stretch' },
});
