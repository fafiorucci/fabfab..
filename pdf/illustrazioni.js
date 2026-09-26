// Illustrazioni vettoriali del ricettario: icone degli ingredienti (viewBox 100×100) e disegni dei piatti (200×160).
// Stile da stampa risograph: una campitura pastello leggermente sfalsata sotto un tratto d'inchiostro.
// Gli elementi con fill="none" sono solo tratto; quelli con class="nf" sono solo colore (niente contorno).

const K = {
  ink: "#3B332C", banana: "#F3DC7A", butter: "#F7EBC0", butterTop: "#FAF1CE", butterSide: "#EFD98F",
  crust: "#DDB27A", flour: "#F2EDE3", apple: "#E9A9A0", appleGreen: "#CFE0A8", cinnamon: "#CFA283",
  milk: "#FBF8F1", lilac: "#9C98C4", lilacPale: "#C9C4DE", bay: "#BCC8A6", onion: "#F0DCCB",
  almond: "#E6D0B8", rose: "#DE93A3", wine: "#CF929B", winePale: "#EBC3C8", champagne: "#F2E2B0",
  sage: "#C5D3B0", bread: "#E3C49C", breadIn: "#F6E9D2", cocoa: "#B98B73", lemon: "#F5E38C",
  egg: "#F4E4CF", grey: "#D9D4CE", glass: "#DDEBEF", chili: "#E8958A", plum: "#B98B9A",
  candied: "#DCE7A6", terracotta: "#D9A58A", roast: "#D9A06E", dark: "#8C6A5A", cream: "#F7EBD8"
};

const P = (d, fill, extra = "") => `<path d="${d}" fill="${fill}" ${extra}/>`;
const C = (cx, cy, r, fill, extra = "") => `<circle cx="${cx}" cy="${cy}" r="${r}" fill="${fill}" ${extra}/>`;
const E = (cx, cy, rx, ry, fill, extra = "") => `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="${fill}" ${extra}/>`;
const G = (t, els) => `<g transform="${t}">${els.join("")}</g>`;
const NF = 'class="nf"';

// ---------- Ingredienti ----------
const ICONS = {
  farina: [
    P("M30 32 C28 24 34 20 40 20 L60 20 C66 20 72 24 70 32 L78 80 C79 86 74 90 68 90 L32 90 C26 90 21 86 22 80 Z", K.flour),
    P("M29 38 C42 44 58 44 71 38", "none"),
    P("M40 20 C44 14 56 14 60 20", "none"),
    P("M50 80 L50 48", "none"),
    E(45.5, 54, 3, 5, K.crust, 'transform="rotate(-25 45.5 54)"'), E(54.5, 54, 3, 5, K.crust, 'transform="rotate(25 54.5 54)"'),
    E(45.5, 63, 3, 5, K.crust, 'transform="rotate(-25 45.5 63)"'), E(54.5, 63, 3, 5, K.crust, 'transform="rotate(25 54.5 63)"'),
    E(50, 46, 2.6, 4.6, K.crust)
  ],
  burro: [
    P("M18 46 L50 33 L84 43 L52 57 Z", K.butterTop),
    P("M18 46 L52 57 L52 78 L18 66 Z", K.butter),
    P("M52 57 L84 43 L84 63 L52 78 Z", K.butterSide),
    P("M30 50 L60 40", "none")
  ],
  zucchero: [
    P("M26 58 C30 36 44 28 50 28 C56 28 70 36 74 58 Z", K.milk),
    P("M16 56 L84 56 C82 78 68 90 50 90 C32 90 18 78 16 56 Z", "#EDE6F0"),
    P("M40 40 L42 42 M56 36 L58 38 M50 46 L52 48", "none")
  ],
  uovo: [
    P("M50 16 C66 16 78 44 78 62 C78 80 66 90 50 90 C34 90 22 80 22 62 C22 44 34 16 50 16 Z", K.egg),
    P("M36 40 C33 48 33 56 35 62", "none")
  ],
  lievito: [
    P("M26 20 L74 20 L74 84 L26 84 Z", "#F6E6DC"),
    P("M26 28 L32 24 L38 28 L44 24 L50 28 L56 24 L62 28 L68 24 L74 28", "none"),
    C(50, 56, 12, K.rose),
    P("M44 56 L56 56 M50 50 L50 62", "none")
  ],
  banana: [
    P("M18 34 C26 70 60 86 86 66 C88 62 85 59 81 61 C62 72 38 62 28 32 Z", K.banana),
    P("M18 34 L14 26 L22 28 Z", K.crust),
    P("M28 44 C38 62 56 70 72 68", "none")
  ],
  mela: [
    P("M50 32 C36 22 18 30 20 52 C22 76 38 90 50 84 C62 90 78 76 80 52 C82 30 64 22 50 32 Z", K.apple),
    P("M50 32 C50 24 52 18 56 14", "none"),
    P("M53 24 C60 14 72 14 76 17 C72 26 61 29 53 24 Z", K.appleGreen),
    P("M32 44 C30 50 30 56 32 60", "none")
  ],
  uvetta: [
    E(34, 40, 11, 8, K.plum, 'transform="rotate(-20 34 40)"'), E(62, 36, 10, 8, K.plum, 'transform="rotate(15 62 36)"'),
    E(46, 62, 12, 8, K.plum, 'transform="rotate(10 46 62)"'), E(72, 62, 9, 7, K.plum, 'transform="rotate(-25 72 62)"'),
    E(30, 72, 9, 7, K.plum, 'transform="rotate(30 30 72)"'),
    P("M28 38 L38 42 M58 34 L66 38 M40 60 L52 64", "none")
  ],
  cedro: [
    P("M20 50 L42 44 L48 66 L26 72 Z", K.candied),
    P("M52 30 L72 28 L74 50 L54 52 Z", K.candied),
    P("M56 60 L78 62 L76 84 L54 82 Z", K.candied),
    C(32, 58, 1.6, K.milk, NF), C(64, 40, 1.6, K.milk, NF), C(66, 72, 1.6, K.milk, NF)
  ],
  limone: [
    P("M14 52 C18 36 34 26 50 26 C66 26 82 36 86 52 C82 68 66 78 50 78 C34 78 18 68 14 52 Z", K.lemon),
    P("M14 52 L8 52 M86 52 L92 52", "none"),
    P("M58 84 C64 78 72 90 80 84", "none"),
    C(36, 44, 1.5, K.milk, NF), C(44, 38, 1.5, K.milk, NF)
  ],
  pane: [
    P("M22 42 C22 26 38 22 50 26 C62 22 78 26 78 42 C78 48 74 50 72 52 L72 86 L28 86 L28 52 C26 50 22 48 22 42 Z", K.bread),
    P("M30 43 C30 32 41 30 50 33 C59 30 70 32 70 43 C70 47 67 49 65 50 L65 80 L35 80 L35 50 C33 49 30 47 30 43 Z", K.breadIn),
    C(44, 56, 1.5, K.bread, NF), C(56, 64, 1.5, K.bread, NF), C(48, 70, 1.5, K.bread, NF)
  ],
  latte: [
    P("M30 16 L70 16 L64 88 L36 88 Z", K.glass),
    P("M31.5 32 L68.5 32 L64 88 L36 88 Z", K.milk),
    P("M40 44 L38 76", "none")
  ],
  cannella: [
    P("M20 68 L66 22 L78 34 L32 80 Z", K.cinnamon),
    P("M24 72 L70 26", "none"),
    P("M34 80 L76 38 L84 46 L42 88 Z", "#DDB595"),
    P("M38 84 L80 42", "none")
  ],
  piccione: [
    P("M16 62 C16 46 32 38 48 40 C56 28 70 24 78 32 C74 34 70 38 70 44 C80 50 88 58 86 66 C72 76 38 80 16 62 Z", K.lilacPale),
    P("M34 54 C46 46 62 50 70 62 C56 66 44 64 34 54 Z", K.lilac),
    P("M78 31 L88 34 L78 38 Z", K.crust),
    C(71, 34, 2.2, K.ink),
    P("M44 76 L42 86 M54 76 L56 86", "none")
  ],
  lardo: [
    P("M16 42 L80 30 L86 60 L22 74 Z", "#FBF1EC"),
    P("M16 42 L80 30 L81.5 38 L17.5 50 Z", "#E9C2B4"),
    P("M30 58 C40 54 50 58 60 52 M40 66 C50 62 62 64 72 58", "none")
  ],
  cipolla: [
    P("M50 14 C54 26 78 40 78 62 C78 80 64 88 50 88 C36 88 22 80 22 62 C22 40 46 26 50 14 Z", K.onion),
    P("M50 22 C40 40 38 70 46 86 M50 22 C60 40 62 70 54 86", "none"),
    P("M44 88 L42 95 M50 88 L50 96 M56 88 L58 95", "none")
  ],
  aceto: [
    P("M38 44 C26 52 24 70 30 82 C36 92 64 92 70 82 C76 70 74 52 62 44 L60 30 L40 30 Z", K.winePale),
    P("M42 30 L42 16 L58 16 L58 30 Z", K.glass),
    C(50, 12, 5, K.cinnamon),
    P("M28 66 C40 70 60 70 72 66", "none")
  ],
  alloro: [
    P("M18 82 C26 44 56 22 84 16 C80 42 60 74 18 82 Z", K.bay),
    P("M18 82 C40 60 60 40 84 16", "none"),
    P("M34 66 L30 52 M46 54 L44 40 M58 42 L58 30 M40 62 L54 64 M52 50 L66 50", "none")
  ],
  chiodo: [
    P("M47 40 L53 40 L55 88 L45 88 Z", K.cocoa),
    C(40, 30, 8, "#A8775E"), C(60, 30, 8, "#A8775E"), C(50, 20, 8, "#A8775E"),
    C(50, 32, 6, K.cinnamon)
  ],
  ginepro: [
    P("M50 14 L44 42 M50 14 L64 36 M47 26 L38 22 M56 24 L64 20", "none"),
    C(40, 56, 12, K.lilac), C(62, 50, 11, K.lilac), C(52, 74, 12, K.lilac),
    P("M36 50 C38 48 40 48 42 48 M58 44 C60 42 62 42 64 42", "none")
  ],
  salepepe: [
    P("M22 42 C22 30 44 30 44 42 L46 86 L20 86 Z", K.milk),
    P("M56 42 C56 30 78 30 78 42 L80 86 L54 86 Z", K.grey),
    C(28, 38, 1.4, K.ink), C(33, 36, 1.4, K.ink), C(38, 38, 1.4, K.ink),
    C(62, 38, 1.4, K.ink), C(67, 36, 1.4, K.ink), C(72, 38, 1.4, K.ink)
  ],
  brodo: [
    P("M18 46 L82 46 L78 84 C78 89 74 91 70 91 L30 91 C26 91 22 89 22 84 Z", K.glass),
    E(50, 46, 32, 5, "#F3E3B5"),
    P("M12 50 L18 50 M82 50 L88 50", "none"),
    P("M38 36 C34 30 42 26 38 18 M50 36 C46 30 54 26 50 18 M62 36 C58 30 66 26 62 18", "none")
  ],
  mandorla: [
    P("M40 14 C56 28 62 50 56 70 C52 82 46 88 40 88 C34 88 28 82 26 70 C22 50 26 30 40 14 Z", K.almond),
    P("M40 24 C34 44 34 66 40 82", "none"),
    P("M68 34 C80 44 84 60 80 74 C78 82 74 86 70 86 C66 86 62 82 60 74 C58 60 60 44 68 34 Z", "#EEDCC8"),
    P("M68 42 C64 56 64 70 69 82", "none")
  ],
  liquore: [
    P("M32 24 L68 24 C68 46 60 56 50 56 C40 56 32 46 32 24 Z", K.glass),
    P("M33.5 34 L66.5 34 C65 48 58 54 50 54 C42 54 35 48 33.5 34 Z", "#DDA893"),
    P("M50 56 L50 80", "none"),
    P("M34 86 C38 80 62 80 66 86 Z", K.glass)
  ],
  vaniglia: [
    P("M18 34 C40 22 70 24 90 14 C74 32 42 36 18 34 Z", K.dark),
    P("M18 60 L82 60 C80 80 68 90 50 90 C32 90 20 80 18 60 Z", "#F6E6DC"),
    P("M26 60 C32 46 44 42 50 42 C56 42 68 46 74 60 Z", K.milk),
    C(42, 52, 1.2, K.dark, NF), C(54, 50, 1.2, K.dark, NF), C(60, 55, 1.2, K.dark, NF)
  ],
  incerto: [
    P("M22 18 L78 22 L74 86 L20 80 Z", "#F6EFD9"),
    P("M40 40 C40 30 60 30 60 40 C60 48 50 48 50 58 M50 68 L50 70", "none")
  ]
};

// Nome dell'ingrediente → icona. L'ordine conta: i casi particolari vengono prima.
const MATCH = [
  [/leggibile, forse/, "incerto"], [/vanigliato|vaniglia/, "vaniglia"], [/farina/, "farina"], [/burro/, "burro"],
  [/zucchero/, "zucchero"], [/uov|tuorl/, "uovo"], [/lievito/, "lievito"], [/banan/, "banana"], [/mele|mela/, "mela"],
  [/uvett/, "uvetta"], [/cedro/, "cedro"], [/limone/, "limone"], [/pane/, "pane"], [/latte/, "latte"],
  [/cannella/, "cannella"], [/piccion/, "piccione"], [/lardo/, "lardo"], [/cipoll/, "cipolla"], [/aceto/, "aceto"],
  [/alloro/, "alloro"], [/garofano/, "chiodo"], [/ginepro/, "ginepro"], [/sale|pepe/, "salepepe"], [/brodo/, "brodo"],
  [/mandorl/, "mandorla"], [/liquore/, "liquore"]
];
const iconFor = nome => (MATCH.find(([re]) => re.test(nome.toLowerCase())) || [null, "incerto"])[1];

// ---------- Piatti ----------
// Gli elementi composti restano separati, uno per gruppo, così la sovrapposizione funziona anche dentro i disegni ripresi.
const Gs = (t, els) => els.map(e => `<g transform="${t}">${e}</g>`);
const icon = (key, t) => Gs(t, ICONS[key]);
const crescent = (x, y, r, fill, inner) => G(`translate(${x} ${y}) rotate(${r})`, [
  P("M-13 0 C-7 -9 7 -9 13 0 C7 -4 -7 -4 -13 0 Z", fill), P("M-10 -1.5 C-5 -5 5 -5 10 -1.5", inner || "none", NF)
]);
const sugar = pts => pts.map(([x, y]) => C(x, y, 1.3, "#FFFFFF", NF)).join("");

const DISHES = {
  "torta-banane": [
    E(100, 124, 90, 22, K.milk),
    P("M36 74 L36 108 C36 122 164 122 164 108 L164 74 Z", K.crust),
    E(100, 74, 64, 17, "#F3D79A"),
    E(72, 70, 8, 4, K.butterTop), E(96, 66, 8, 4, K.butterTop), E(122, 70, 8, 4, K.butterTop), E(88, 80, 8, 4, K.butterTop), E(112, 81, 8, 4, K.butterTop),
    C(72, 70, 1.2, K.cocoa, NF), C(96, 66, 1.2, K.cocoa, NF), C(122, 70, 1.2, K.cocoa, NF), C(88, 80, 1.2, K.cocoa, NF), C(112, 81, 1.2, K.cocoa, NF),
    P("M36 92 C80 100 120 100 164 92", "none"),
    icon("banana", "translate(132 96) scale(.55)")
  ],
  "torta-mele": [
    E(100, 96, 88, 44, K.milk),
    E(100, 92, 72, 32, "#EACB8E"),
    crescent(70, 84, -20, K.apple, "#F7E3B7"), crescent(96, 78, 5, K.apple, "#F7E3B7"), crescent(124, 84, 20, K.apple, "#F7E3B7"),
    crescent(80, 102, -10, K.apple, "#F7E3B7"), crescent(110, 104, 12, K.apple, "#F7E3B7"),
    C(88, 90, 2.4, K.plum), C(116, 92, 2.4, K.plum), C(66, 96, 2.4, K.plum), C(132, 98, 2.4, K.plum), C(100, 94, 2.2, K.candied),
    P("M12 96 L4 94 M188 96 L196 94", "none"),
    icon("mela", "translate(150 8) scale(.42)")
  ],
  "piccioni-ginepro": [
    P("M30 72 L170 72 L162 124 C160 133 150 138 140 138 L60 138 C50 138 40 133 38 124 Z", K.terracotta),
    E(100, 72, 72, 15, "#C98E73"),
    E(100, 73, 62, 10, "#9E6E57"),
    E(78, 68, 22, 12, K.roast), E(122, 68, 22, 12, K.roast),
    P("M62 64 L94 64 M106 64 L138 64", "none"),
    C(100, 76, 3, K.lilac), C(64, 76, 3, K.lilac), C(138, 76, 3, K.lilac),
    P("M26 84 C18 84 18 96 28 96 M174 84 C182 84 182 96 172 96", "none"),
    icon("alloro", "translate(146 102) scale(.4)")
  ],
  "torta-cinque-minuti": [
    E(100, 122, 90, 22, K.milk),
    P("M30 86 L30 104 C30 122 170 122 170 104 L170 86 Z", "#D9B48A"),
    E(100, 86, 70, 21, "#EBD3AE"),
    sugar([[70, 82], [84, 76], [100, 80], [116, 76], [130, 84], [92, 90], [110, 92], [76, 92], [124, 94], [100, 72], [140, 88], [60, 88]]),
    P("M30 94 C70 102 130 102 170 94", "none"),
    icon("mandorla", "translate(14 104) scale(.34)"), icon("mandorla", "translate(156 100) scale(.3) rotate(20 50 50)")
  ],
  crostini: [
    P("M16 76 L164 62 C170 62 172 66 172 70 L176 100 C176 104 172 107 168 107 L22 118 C18 118 16 115 16 112 Z", K.bread),
    P("M176 80 L192 78 L193 90 L177 92", "none"),
    E(52, 92, 20, 11, "#F0D9A8"), E(94, 88, 20, 11, "#F0D9A8"), E(136, 84, 20, 11, "#F0D9A8"),
    E(52, 90, 13, 6, "#9C6B5A"), E(94, 86, 13, 6, "#9C6B5A"), E(136, 82, 13, 6, "#C98E73"),
    C(48, 88, 2, K.bay, NF), C(98, 84, 2, K.bay, NF), C(132, 80, 2, K.bay, NF)
  ],
  spaghetti: [
    E(100, 96, 88, 40, K.milk),
    E(100, 92, 60, 24, "#F6E7AE"),
    P("M60 92 C60 76 140 76 140 92 C140 108 70 108 72 92 C74 80 128 80 128 92 C128 102 84 102 86 92 C88 86 114 86 114 92", "none"),
    G("translate(126 70) rotate(25)", [P("M0 0 C8 -2 20 2 26 10 C18 10 6 8 0 0 Z", K.chili), P("M0 0 L-5 -3", "none")]),
    E(80, 84, 4, 2.6, "#FFFFFF"), E(108, 102, 4, 2.6, "#FFFFFF"), E(96, 78, 4, 2.6, "#FFFFFF"),
    C(70, 98, 1.5, K.bay, NF), C(120, 96, 1.5, K.bay, NF)
  ],
  pagnotta: [
    E(100, 132, 84, 12, K.milk),
    P("M24 128 C24 76 58 52 100 52 C142 52 176 76 176 128 Z", K.bread),
    P("M42 84 C70 40 130 40 158 84 C130 72 70 72 42 84 Z", "#D9B07E"),
    P("M60 104 L78 92 M92 110 L110 98 M124 104 L142 92", "none"),
    P("M86 44 C82 36 90 32 86 24 M104 42 C100 34 108 30 104 22", "none"),
    icon("alloro", "translate(146 96) scale(.36)")
  ],
  insalata: [
    P("M40 78 C30 58 56 40 70 58 C72 40 100 34 104 56 C112 38 144 42 138 64 C156 60 168 74 158 84 Z", K.appleGreen),
    P("M58 70 C66 56 80 58 86 72 M110 66 C118 56 132 58 136 72", "none"),
    C(90, 72, 7, K.apple), C(120, 76, 6, K.apple),
    P("M24 80 L176 80 C174 116 142 136 100 136 C58 136 26 116 24 80 Z", "#EDE6F0"),
    P("M40 96 C80 104 120 104 160 96", "none")
  ],
  tiramisu: [
    P("M28 72 L150 60 L176 88 L54 102 Z", K.cocoa),
    P("M28 72 L54 102 L54 128 L28 96 Z", K.cream),
    P("M54 102 L176 88 L176 114 L54 128 Z", "#FBF3E6"),
    P("M54 110 L176 96 M54 119 L176 105", "none"),
    P("M28 80 L54 110 M28 88 L54 119", "none"),
    C(70, 80, 1.4, "#8C6A5A", NF), C(100, 76, 1.4, "#8C6A5A", NF), C(130, 72, 1.4, "#8C6A5A", NF), C(110, 88, 1.4, "#8C6A5A", NF), C(146, 84, 1.4, "#8C6A5A", NF)
  ],
  frutta: [
    icon("mela", "translate(34 34) scale(.52)"),
    P("M104 44 C98 44 96 54 94 62 C86 70 84 84 92 92 C100 100 116 98 120 88 C124 78 118 68 112 62 C110 54 110 44 104 44 Z", K.appleGreen),
    P("M104 44 L106 36", "none"),
    C(128, 58, 7, K.lilac), C(140, 58, 7, K.lilac), C(134, 70, 7, K.lilac), C(146, 70, 7, K.lilac), C(140, 82, 7, K.lilac),
    P("M134 50 L138 40", "none"),
    P("M24 86 L176 86 C172 118 140 134 100 134 C60 134 28 118 24 86 Z", K.almond),
    P("M36 100 C80 108 120 108 164 100", "none")
  ],
  caffe: [
    E(70, 122, 50, 12, K.milk),
    P("M42 76 L98 76 C98 106 88 118 70 118 C52 118 42 106 42 76 Z", K.milk),
    E(70, 76, 28, 6, K.dark),
    P("M98 84 C112 84 112 102 96 102", "none"),
    P("M60 64 C56 56 64 52 60 44 M76 64 C72 56 80 52 76 44", "none"),
    P("M128 34 L140 34 L140 54 C150 60 152 70 152 80 L152 132 L116 132 L116 80 C116 70 118 60 128 54 Z", K.wine),
    P("M120 90 L148 90 L148 112 L120 112 Z", K.milk),
    P("M160 60 L168 60 L168 74 C176 80 178 88 178 96 L178 132 L150 132", K.sage)
  ],
  champagne: [
    P("M60 22 L88 22 C88 62 80 80 74 80 C68 80 60 62 60 22 Z", K.champagne),
    P("M74 80 L74 124", "none"),
    E(74, 128, 16, 4, K.glass),
    C(70, 40, 1.8, "#FFFFFF", NF), C(76, 52, 1.6, "#FFFFFF", NF), C(72, 64, 1.4, "#FFFFFF", NF), C(78, 34, 1.4, "#FFFFFF", NF),
    P("M126 24 L140 24 L140 50 C154 58 158 70 158 86 L158 140 L108 140 L108 86 C108 70 112 58 126 50 Z", K.sage),
    P("M124 18 L142 18 L142 44 L124 44 Z", K.champagne),
    P("M112 96 L154 96 L154 122 L112 122 Z", K.milk)
  ],
  rosso: [
    P("M40 56 L96 56 C96 94 84 108 68 108 C52 108 40 94 40 56 Z", K.glass),
    P("M41 78 L95 78 C93 98 82 106 68 106 C54 106 43 98 41 78 Z", K.wine),
    P("M68 108 L68 132", "none"),
    E(68, 136, 18, 4, K.glass),
    P("M128 22 L142 22 L142 50 C154 56 158 68 158 82 L158 140 L112 140 L112 82 C112 68 116 56 128 50 Z", K.wine),
    P("M116 92 L154 92 L154 120 L116 120 Z", K.milk),
    P("M124 104 L146 104", "none")
  ]
};
// La tavola della prima cena: pagnotta al centro, champagne e rosso ai lati.
DISHES["prima-cena"] = [
  Gs("translate(-30 30) scale(.56)", DISHES.champagne.flat()),
  Gs("translate(86 30) scale(.56)", DISHES.rosso.flat()),
  Gs("translate(38 48) scale(.62)", DISHES.pagnotta.flat())
];
for (const k in DISHES) DISHES[k] = DISHES[k].flat();

const DISH_BY_NAME = [
  [/crostini/i, "crostini"], [/spaghetti/i, "spaghetti"], [/pagnotta/i, "pagnotta"], [/insalata/i, "insalata"],
  [/tiramis/i, "tiramisu"], [/frutta/i, "frutta"], [/caff/i, "caffe"], [/champagne/i, "champagne"], [/rosso/i, "rosso"]
];
const dishFor = nome => (DISH_BY_NAME.find(([re]) => re.test(nome)) || [null, null])[1];

const svg = (els, vb, cls = "") => {
  const off = vb === "0 0 100 100" ? 2.6 : 3.4;
  // Ogni elemento disegna prima il colore sfalsato e poi il tratto: chi sta davanti copre le linee di chi sta dietro.
  const body = els.map(el => `<g class="fl" transform="translate(${off} ${off})">${el}</g><g class="ol">${el}</g>`).join("");
  return `<svg class="ill ${cls}" viewBox="${vb}" xmlns="http://www.w3.org/2000/svg">${body}</svg>`;
};
const iconSvg = (key, cls) => svg(ICONS[key], "0 0 100 100", cls);
const dishSvg = (key, cls) => svg(DISHES[key], "0 0 200 160", cls);

// Regole di stile da includere nel foglio della pagina.
const ILL_CSS = `
  .ill { display: block; overflow: visible; }
  .ill .fl * { stroke: none; }
  .ill .fl [fill="none"] { display: none; }
  .ill .ol * { fill: none; stroke: ${K.ink}; stroke-width: 1.15px; vector-effect: non-scaling-stroke; stroke-linecap: round; stroke-linejoin: round; }
  .ill .ol .nf { display: none; }`;

module.exports = { ICONS, DISHES, iconFor, dishFor, iconSvg, dishSvg, ILL_CSS };
