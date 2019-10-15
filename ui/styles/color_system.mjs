// Grays
const grays = {
    "000": "#fafbfc",
    "100": "#f6f8fa",
    "200": "#e1e4e8",
    "300": "#d1d5da",
    "400": "#959da5",
    "500": "#6a737d",
    "600": "#586069",
    "700": "#444d56",
    "800": "#2f363d",
    "900": "#24292e"
}

// Blues
const blues = {
    "000": '#f1f8ff',
    "100": '#dbedff',
    "200": '#c8e1ff',
    "300": '#79b8ff',
    "400": '#2188ff',
    "500": '#0366d6',
    "600": '#005cc5',
    "700": '#044289',
    "800": '#032f62',
    "900": '#05264c'
}

// Greens
const greens = {
    "000": '#f0fff4',
    "100": '#dcffe4',
    "200": '#bef5cb',
    "300": '#85e89d',
    "400": '#34d058',
    "500": '#28a745',
    "600": '#22863a',
    "700": '#176f2c',
    "800": '#165c26',
    "900": '#144620'
}

// Yellows
const yellows = {
    "000": '#fffdef',
    '100': '#fffbdd',
    '200': '#fff5b1',
    '300': '#ffea7f',
    '400': '#ffdf5d',
    '500': '#ffd33d',
    '600': '#f9c513',
    '700': '#dbab09',
    '800': '#b08800',
    '900': '#735c0f'
}

// Oranges
const oranges = {
    '000': '#fff8f2',
    '100': '#ffebda',
    '200': '#ffd1ac',
    '300': '#ffab70',
    '400': '#fb8532',
    '500': '#f66a0a',
    '600': '#e36209',
    '700': '#d15704',
    '800': '#c24e00',
    '900': '#a04100'
}

// Reds
const reds = {
    '000': '#ffeef0',
    '100': '#ffdce0',
    '200': '#fdaeb7',
    '300': '#f97583',
    '400': '#ea4a5a',
    '500': '#d73a49',
    '600': '#cb2431',
    '700': '#b31d28',
    '800': '#9e1c23',
    '900': '#86181d'
}

const purples = {
    '000': '#f5f0ff',
    '100': '#e6dcfd',
    '200': '#d1bcf9',
    '300': '#b392f0',
    '400': '#8a63d2',
    '500': '#6f42c1',
    '600': '#5a32a3',
    '700': '#4c2889',
    '800': '#3a1d6e',
    '900': '#29134e'
}

const pinks = {
    '000': '#ffeef8',
    '100': '#fedbf0',
    '200': '#f9b3dd',
    '300': '#f692ce',
    '400': '#ec6cb9',
    '500': '#ea4aaa',
    '600': '#d03592',
    '700': '#b93a86',
    '800': '#99306f',
    '900': '#6d224f'
}

const allColors = {
    'gray': grays,
    'blue': blues,
    'green': greens,
    'yellow': yellows,
    'orange': oranges,
    'red': reds,
    'purple': purples,
    'pink': pinks
}

export function getColor(name, index) {
    return allColors[name][index.toString()]
}

// add alpha to color with format '#xxxxxx' or '#xxx'
export function hexPlusAlpha(hex, alpha) {
    if (/^#([A-Fa-f0-9]{3}){1,2}$/.test(hex)) {
        let c = hex.substring(1).split('')
        if (c.length === 3) {
            c = [c[0], c[0], c[1], c[1], c[2], c[2]]
        }
        let a = (Math.floor(alpha * 255)).toString(16)
        if (a.length === 1)
            a = ['0', a[0]]
        else if (a.length === 0)
            a = ['0', '0']
        c = [a[0], a[1], c[0], c[1], c[2], c[3], c[4], c[5]]
        c = '#' + c.join('')
        return c
    } else
        return hex
}

// Fades
export const black = '#1b1f23'
export const white = '#fff'

export const black_fade_15 = hexPlusAlpha(black, 0.15)
export const black_fade_30 = hexPlusAlpha(black, 0.3)
export const black_fade_50 = hexPlusAlpha(black, 0.5)
export const black_fade_70 = hexPlusAlpha(black, 0.7)
export const black_fade_85 = hexPlusAlpha(black, 0.85)

export const white_fade_15 = hexPlusAlpha(white, 0.15)
export const white_fade_30 = hexPlusAlpha(white, 0.3)
export const white_fade_50 = hexPlusAlpha(white, 0.5)
export const white_fade_70 = hexPlusAlpha(white, 0.7)
export const white_fade_85 = hexPlusAlpha(white, 0.85)

// Color defaults
export const red = reds['500']
export const purple = purples['500']
export const blue = blues['500']
export const green = greens['500']
export const yellow = yellows['500']
export const orange = oranges['500']
export const gray_dark = grays['900']
export const gray_light = grays['400']
export const gray = grays['500']

// code from https://github.com/PimpTrizkit/PJs/wiki/12.-Shade,-Blend-and-Convert-a-Web-Color-(pSBC.js)
// Version 4.0
const pSBC = (p, c0, c1, l) => {
    let r, g, b, P, f, t, h, i = parseInt, m = Math.round, a = typeof (c1) == "string";
    if (typeof (p) != "number" || p < -1 || p > 1 || typeof (c0) != "string" || (c0[0] != 'r' && c0[0] != '#') || (c1 && !a)) return null;
    if (!pSBC.pSBCr) pSBC.pSBCr = (d) => {
        let n = d.length, x = {};
        if (n > 9) {
            [r, g, b, a] = d = d.split(","), n = d.length;
            if (n < 3 || n > 4) return null;
            x.r = i(r[3] == "a" ? r.slice(5) : r.slice(4)), x.g = i(g), x.b = i(b), x.a = a ? parseFloat(a) : -1
        } else {
            if (n == 8 || n == 6 || n < 4) return null;
            if (n < 6) d = "#" + d[1] + d[1] + d[2] + d[2] + d[3] + d[3] + (n > 4 ? d[4] + d[4] : "");
            d = i(d.slice(1), 16);
            if (n == 9 || n == 5) x.r = d >> 24 & 255, x.g = d >> 16 & 255, x.b = d >> 8 & 255, x.a = m((d & 255) / 0.255) / 1000;
            else x.r = d >> 16, x.g = d >> 8 & 255, x.b = d & 255, x.a = -1
        }
        return x
    };
    h = c0.length > 9, h = a ? c1.length > 9 ? true : c1 == "c" ? !h : false : h, f = pSBC.pSBCr(c0), P = p < 0, t = c1 && c1 != "c" ? pSBC.pSBCr(c1) : P ? {
        r: 0,
        g: 0,
        b: 0,
        a: -1
    } : {r: 255, g: 255, b: 255, a: -1}, p = P ? p * -1 : p, P = 1 - p;
    if (!f || !t) return null;
    if (l) r = m(P * f.r + p * t.r), g = m(P * f.g + p * t.g), b = m(P * f.b + p * t.b);
    else r = m((P * f.r ** 2 + p * t.r ** 2) ** 0.5), g = m((P * f.g ** 2 + p * t.g ** 2) ** 0.5), b = m((P * f.b ** 2 + p * t.b ** 2) ** 0.5);
    a = f.a, t = t.a, f = a >= 0 || t >= 0, a = f ? a < 0 ? t : t < 0 ? a : a * P + t * p : 0;
    if (h) return "rgb" + (f ? "a(" : "(") + r + "," + g + "," + b + (f ? "," + m(a * 1000) / 1000 : "") + ")";
    else return "#" + (4294967296 + r * 16777216 + g * 65536 + b * 256 + (f ? m(a * 255) : 0)).toString(16).slice(1, f ? undefined : -2)
}

export function darken(color, amt) {
    return pSBC(-amt, color)
}

export function lighter(color,amt) {
    return pSBC(amt,color)
}