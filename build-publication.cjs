// Run: node build-publication.cjs [https://your-domain.com/]
// Without a domain, create a preview package excluded from search indexing.
const fs = require('node:fs');
const path = require('node:path');
const root = __dirname;
const domain = process.argv[2];
let origin;
if (domain) {
  const url = new URL(domain);
  if (url.protocol !== 'https:' || url.username || url.password || url.search || url.hash || url.pathname !== '/' || !url.hostname.includes('.') || /DOMAIN-ANDA/i.test(url.hostname)) {
    throw new Error('Use the final HTTPS domain without a path, query, or fragment.');
  }
  origin = url.origin;
}
const mode = origin ? 'production' : 'preview';
const stamp = new Date().toISOString().replace(/[:.]/g, '-');
const destination = path.join(root, 'release', `${mode}-${stamp}`);
fs.mkdirSync(destination, { recursive: true });
let html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
// Remove working instructions and inactive placeholder metadata from the public HTML.
html = html.replace(/<!--[\s\S]*?-->/g, '');
if (origin) {
  html = html.replace('</head>', `  <link rel="canonical" href="${origin}/">\n  <meta property="og:url" content="${origin}/">\n</head>`);
  html = html.replace(/content="Aset\/social-preview-mohamad-arif-pramarta.jpg"/g, `content="${origin}/Aset/social-preview-mohamad-arif-pramarta.jpg"`);
  const modified = fs.statSync(path.join(root, 'index.html')).mtime.toISOString().slice(0, 10);
  fs.writeFileSync(path.join(destination, 'sitemap.xml'), `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>${origin}/</loc><lastmod>${modified}</lastmod></url></urlset>\n`);
} else {
  html = html.replace('content="index,follow,max-image-preview:large"', 'content="noindex,follow"');
}
fs.writeFileSync(path.join(destination, 'index.html'), html);
fs.writeFileSync(path.join(destination, 'robots.txt'), `User-agent: *\nAllow: /\n${origin ? `Sitemap: ${origin}/sitemap.xml\n` : ''}`);
// Explicit allowlist: no CVs, reference documents, source images, or audit files.
const assets = [
  'Aset/favicon-transparent-32.png',
  'Aset/apple-touch-icon-transparent.png',
  'Aset/social-preview-mohamad-arif-pramarta.jpg',
  'Aset/hero-data-scene.css',
  'Aset/hero-data-scene.js',
  'Aset/client-logos.css',
  'Aset/landing.css',
  'Aset/client-logos.js',
  'Foto/portrait-semi-formal-640.webp',
  'Foto/portrait-semi-formal-960.webp',
  'Foto/portrait-semi-formal-960.jpg',
  'Logo Klien/web/bappenas.webp',
  'Logo Klien/web/icg.webp',
  'Logo Klien/web/indekstat.webp',
  'Logo Klien/web/bright-sinergi-global.webp',
];
for (const asset of assets) {
  const target = path.join(destination, asset);
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.copyFileSync(path.join(root, asset), target);
}
// Halaman 404 statis: Cloudflare Pages menampilkannya otomatis untuk alamat yang tidak ada.
const notFound = fs.readFileSync(path.join(root, '404.html'), 'utf8').replace(/<!--[\s\S]*?-->/g, '');
fs.writeFileSync(path.join(destination, '404.html'), notFound);
if (/DOMAIN-ANDA/i.test(html)) throw new Error('Placeholder remains in public HTML.');
console.log(destination);
