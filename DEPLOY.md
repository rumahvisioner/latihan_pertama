# Checklist deploy landing page

## Paket pratinjau terbaru — 17 September 2026

Paket ini menggantikan ZIP 16 September. Perubahan yang sudah masuk:

- Tampilan utama dipindah ke `Aset/landing.css`, kontras teks keterangan grafik diperbaiki, deskripsi mesin pencari diperbarui, dan email dihapus dari data terstruktur.
- Kolom Nomor WhatsApp (tidak wajib) pada formulir; nomor ikut masuk ke email, draf Gmail, dan Salin Ringkasan.
- Testimoni tampil 3 kartu sekaligus di layar lebar dan dapat digeser; di ponsel tetap satu per satu.
- Kartu harga: Konsultasi mulai Rp2 juta/proyek (dengan asumsi singkat dan contoh SKM), Workshop mulai Rp350 ribu/sesi ±2 jam (dengan daftar fasilitas termasuk sertifikat Yayasan Lentera Visioner Indonesia).
- Bukti ulasan Superprof pada kartu privat: 5,0 dari 14 ulasan, 38 murid, lencana "Duta Besar" (diperiksa September 2026; perbarui bila berubah).
- Kalimat pengalaman di hero, keterangan "kini Komdigi", FAQ kesediaan menandatangani NDA, judul tab baru, dan data terstruktur (harga awal) untuk mesin pencari.
- Foto cadangan JPG diganti `Foto/portrait-semi-formal-960.jpg` (±84 KB, sebelumnya ±490 KB).
- Halaman `404.html` baru untuk alamat yang tidak ditemukan.
- Kebijakan Privasi kini menyebut Cloudflare Web Analytics tanpa cookie. **Aktifkan fitur tersebut setelah deploy (lihat bagian F2)** agar pernyataan ini akurat.

Domain utama belum ditentukan. Gunakan ZIP `release/landing-page-preview-2026-09-17.zip` untuk deployment sementara. ZIP ini hanya memuat HTML dan aset yang diperlukan situs; `index.html` dan `404.html` berada langsung di akar ZIP. ZIP 16 September sudah usang dan tidak boleh diunggah.

Paket pratinjau memakai `noindex,follow`, tidak menyertakan sitemap domain contoh, dan belum memiliki canonical atau URL gambar sosial absolut. Penanda noindex bukan pembatas akses: siapa pun yang mengetahui alamat pratinjau tetap dapat membukanya. Jangan memakai paket ini sebagai rilis produksi final.

Paket dapat dibuat ulang dengan `node build-publication.cjs`. Setelah domain dipilih, jalankan `node build-publication.cjs https://domain-final-anda.com/` dengan alamat utama yang sebenarnya. Pembuat paket akan menghasilkan folder produksi baru dengan canonical, og:url, URL gambar sosial absolut, robots.txt, dan sitemap; berkas sumber tetap menjadi templat kerja. Gunakan keluaran produksi tersebut untuk unggahan final, bukan ZIP pratinjau.

Paket pratinjau telah diuji melalui server lokal pada lebar 320, 390, 768, 1024, dan 1440 piksel. Menu ponsel, tab layanan, tombol harga, carousel, dan formulir lokal bekerja. Aktivasi FormSubmit, penerimaan email nyata, HTTPS, dan pratinjau berbagi masih perlu diuji setelah deployment. Paket ini belum diunggah ke hosting.

Panduan manual di bawah tetap tersedia sebagai alternatif; jangan mencampur berkas sumber dengan hasil paket otomatis saat mengunggah.

Landing page ini adalah situs statis. Berkas utama yang dibuka pengunjung adalah `index.html`.

## Jalur yang disarankan untuk proyek ini

Gunakan **Cloudflare Pages melalui Direct Upload**. Halaman sudah berisi HTML, CSS, JavaScript, dan aset siap pakai sehingga tidak memerlukan proses build, basis data, atau server aplikasi.

Alur lengkapnya:

```text
Tentukan domain dan alamat utama
        ↓
Isi domain ke metadata halaman
        ↓
Buat folder publikasi yang bersih
        ↓
Uji folder publikasi melalui server lokal
        ↓
Unggah ke Cloudflare Pages
        ↓
Periksa alamat sementara .pages.dev
        ↓
Hubungkan domain dan tunggu HTTPS aktif
        ↓
Aktifkan serta uji FormSubmit
        ↓
Periksa tampilan dan pratinjau berbagi
        ↓
Daftarkan domain ke Google Search Console
```

Direct Upload cocok jika pembaruan situs dilakukan manual dari folder ini. Jika sejak awal ingin setiap perubahan di GitHub otomatis dipublikasikan, pilih integrasi Git ketika membuat proyek. Cloudflare tidak menyediakan perubahan langsung dari proyek Direct Upload menjadi proyek dengan integrasi Git; untuk berpindah, proyek baru perlu dibuat.

## Informasi yang perlu diputuskan terlebih dahulu

Catat empat informasi ini sebelum mulai:

```text
Domain yang dibeli       : ______________________________
Alamat utama situs       : https://______________________/
Nama proyek Cloudflare   : ______________________________
Metode deploy            : Direct Upload / Git
```

Untuk alamat utama, pilih salah satu pola berikut:

- `https://domainanda.com/` sebagai alamat utama, lalu `www.domainanda.com` diarahkan ke sana; atau
- `https://www.domainanda.com/` sebagai alamat utama, lalu `domainanda.com` diarahkan ke sana.

Untuk situs personal yang pendek, alamat tanpa `www` biasanya lebih ringkas. Gunakan pilihan yang sama pada metadata, sitemap, Search Console, dan semua materi promosi.

## Prosedur terperinci menggunakan Cloudflare Pages

### A. Buat akun dan siapkan domain

1. Buat atau masuk ke akun Cloudflare.
2. Jika domain belum dibeli, beli melalui registrar pilihan Anda.
3. Pastikan Anda dapat membuka panel DNS domain dan email yang dipakai untuk akun registrar.
4. Pastikan Anda juga dapat membuka `arifpramarta@gmail.com`, karena konfirmasi FormSubmit akan dikirim ke alamat tersebut.
5. Jangan memindahkan DNS atau mengganti *nameserver* sebelum situs berhasil dibuka melalui alamat sementara Cloudflare.

### B. Berikan domain final untuk penyelesaian metadata

Sebelum folder diunggah, lakukan perubahan berikut pada `index.html`:

1. Cari `https://DOMAIN-ANDA.com/`.
2. Ganti dengan alamat utama lengkap, termasuk `https://` dan garis miring penutup.
3. Hapus tanda komentar di sekitar `canonical` dan `og:url` agar kedua tag aktif.
4. Ubah `og:image` menjadi URL absolut, misalnya:

   ```text
   https://domainanda.com/Aset/social-preview-mohamad-arif-pramarta.jpg
   ```

5. Gunakan URL gambar yang sama pada `twitter:image`.
6. Pada `robots.txt`, ganti alamat sitemap menjadi:

   ```text
   Sitemap: https://domainanda.com/sitemap.xml
   ```

7. Pada `sitemap.xml`, ganti isi `<loc>` dengan alamat utama.
8. Isi `<lastmod>` dengan tanggal publikasi dalam format `YYYY-MM-DD`.
9. Pastikan pencarian `DOMAIN-ANDA.com` pada `index.html`, `robots.txt`, dan `sitemap.xml` tidak menghasilkan temuan.
10. `index.html` adalah satu-satunya berkas HTML kerja; salinan `Hero_Landing_Page_Mohamad_Arif_Pramarta.html` sudah dihapus pada 17 September 2026.

Tahap ini sebaiknya saya kerjakan setelah Anda memberikan domain dan pilihan `www`, karena salah ketik pada canonical atau sitemap dapat membuat mesin pencari mengenali alamat yang keliru.

### C. Buat folder publikasi yang bersih

1. Buat folder baru bernama, misalnya, `landing-page-publikasi` di luar folder proyek atau di folder sementara.
2. Salin hanya `index.html`, `404.html`, `robots.txt`, `sitemap.xml`, serta berkas pada folder `Aset`, `Foto`, dan `Logo Klien` sesuai daftar di Lampiran bagian 2.
3. Di dalam `Logo Klien`, sisakan folder `web` beserta empat gambar WebP. PNG sumber tidak perlu dimasukkan. Cara paling aman: jalankan `node build-publication.cjs`, karena skrip hanya menyalin berkas yang diperlukan.
4. Buka folder publikasi dan pastikan `index.html` langsung terlihat pada tingkat teratas.
5. Jangan membuat susunan seperti `landing-page-publikasi/folder-lain/index.html`; struktur tersebut dapat menyebabkan halaman utama tidak ditemukan.
6. Jika ingin memakai ZIP, pilih **isi** folder publikasi lalu kompres. Setelah ZIP dibuka, `index.html` harus langsung terlihat, bukan berada satu tingkat lebih dalam.
7. Simpan satu salinan ZIP tersebut sebagai versi rilis pertama, misalnya `landing-page-v1-YYYY-MM-DD.zip`.

### D. Uji folder publikasi sebelum diunggah

Jalankan situs melalui server lokal dari folder publikasi. Halaman yang dibuka harus menggunakan alamat seperti `http://localhost:...`, bukan `file:///...`.

Periksa hasil yang diharapkan berikut:

| Bagian | Tindakan | Hasil yang diharapkan |
|---|---|---|
| Header | Klik setiap menu | Halaman berpindah ke bagian yang benar |
| Menu ponsel | Buka dan pilih menu | Menu tertutup setelah pilihan ditekan |
| Layanan | Pilih tiga tab | Panel sesuai pilihan muncul |
| Pengalaman | Buka daftar lengkap | Semua proyek dapat dibaca |
| Testimoni | Pilih filter dan panah | Daftar dan penghitung berubah dengan benar |
| Harga | Klik tiga tombol layanan | Jenis layanan pada formulir terpilih otomatis |
| FAQ | Buka setiap pertanyaan | Jawaban tampil dan tidak terpotong |
| Formulir | Kirim tanpa isian | Kolom wajib ditandai oleh browser |
| Formulir lokal | Isi lalu kirim | Pilihan Gmail dan salin ringkasan muncul |
| Tautan luar | Buka LinkedIn, Tableau, Superprof | Alamat tujuan benar dan terbuka di tab baru |
| Testimoni lebar | Buka pada lebar 1440 piksel | Tiga kartu tampil, panah dan titik menggeser satu kartu |
| Kolom WhatsApp | Isi huruf atau nomor pendek | Browser menolak isian yang tidak valid |
| Halaman 404 | Buka `/alamat-asal` | Halaman "Halaman tidak ditemukan" tampil |

Uji minimal pada lebar layar sekitar 390 piksel dan 1440 piksel. Pastikan tidak ada teks atau kartu yang melebar keluar layar.

### E. Buat proyek Cloudflare Pages

1. Buka dasbor Cloudflare.
2. Masuk ke **Workers & Pages**.
3. Pilih **Create application**.
4. Pilih opsi untuk memulai Pages dan **Drag and drop your files** atau **Direct Upload**. Nama tombol dapat sedikit berubah, tetapi cari jalur unggah aset statis dari komputer.
5. Masukkan nama proyek. Gunakan huruf kecil dan tanda hubung, misalnya `mohamad-arif-pramarta`.
6. Nama proyek akan membentuk alamat sementara seperti `mohamad-arif-pramarta.pages.dev`.
7. Seret folder publikasi atau ZIP yang sudah diperiksa ke area unggahan.
8. Periksa daftar unggahan; tidak boleh ada tanda gagal pada `index.html` atau aset gambar.
9. Pilih **Deploy site**.
10. Tunggu status deployment berhasil, lalu buka alamat `.pages.dev` yang diberikan.

Pada Direct Upload tidak ada *framework preset*, *build command*, atau *output directory* yang perlu diisi. Jika Anda melihat formulir pengaturan build, kemungkinan jalur Git yang dipilih, bukan Direct Upload.

### F. Periksa deployment sementara

Pada alamat `.pages.dev`, periksa:

1. Halaman utama langsung terbuka tanpa `/index.html`.
2. Foto profil, ikon, gambar sosial jika dibuka langsung, dan empat logo klien tampil.
3. Tidak ada alamat aset yang menghasilkan 404.
4. Menu, tab layanan, testimoni, FAQ, dan formulir bekerja.
5. Buka Developer Tools hanya jika ada masalah, lalu periksa apakah ada pesan merah pada Console atau Network.
6. Jangan membagikan alamat `.pages.dev` untuk promosi. Gunakan alamat tersebut hanya untuk pemeriksaan awal.

### F2. Aktifkan penghitung pengunjung tanpa cookie (wajib)

Kebijakan Privasi menyebut Cloudflare Web Analytics, jadi fitur ini perlu diaktifkan:

1. Buka proyek Pages di dasbor Cloudflare.
2. Masuk ke tab **Metrics** (atau **Analytics**), lalu cari **Web Analytics**.
3. Pilih **Enable**. Cloudflare akan menyisipkan skrip penghitung secara otomatis pada deployment berikutnya; tidak perlu mengubah `index.html`.
4. Lakukan deploy ulang (unggah ulang ZIP yang sama) agar skrip ikut terpasang.
5. Buka situs, tunggu beberapa menit, lalu pastikan kunjungan tercatat di menu **Web Analytics**.
6. Jika memilih hosting selain Cloudflare, ubah kalimat analitik pada Kebijakan Privasi di `index.html` sebelum unggah.

### G. Hubungkan domain final

1. Buka proyek Pages di Cloudflare.
2. Masuk ke **Custom domains**.
3. Pilih **Set up a domain**.
4. Masukkan alamat utama yang telah dipilih.
5. Jika memakai domain utama tanpa subdomain, misalnya `domainanda.com`, domain perlu ditambahkan sebagai zona Cloudflare dan *nameserver* di registrar diarahkan ke dua *nameserver* yang diberikan Cloudflare.
6. Salin kedua *nameserver* secara persis ke pengaturan domain pada registrar. Hapus *nameserver* lama hanya pada formulir yang memang ditujukan untuk penggantian *nameserver*.
7. Jika memakai subdomain seperti `jasa.domainanda.com` sementara DNS tetap dikelola di tempat lain, buat CNAME sesuai nilai yang ditampilkan Cloudflare, biasanya menuju `<nama-proyek>.pages.dev`.
8. Kembali ke halaman **Custom domains** dan tunggu status berubah menjadi aktif.
9. Jangan membuat CNAME manual sebelum domain ditambahkan melalui menu **Custom domains**, karena Cloudflare perlu mengaitkan nama tersebut dengan proyek Pages.
10. Propagasi DNS dapat berlangsung cepat atau memerlukan beberapa jam. Jangan berkali-kali mengganti record selama proses masih berjalan.

### H. Pastikan HTTPS dan satu alamat utama

1. Buka `http://domainanda.com` dan pastikan berpindah ke `https://`.
2. Periksa ikon koneksi aman pada browser.
3. Buka versi `www` dan versi tanpa `www`.
4. Pilih satu versi sebagai alamat utama; versi lain harus mengarah dengan status permanen 301.
5. Pada Cloudflare, pengalihan host dapat dibuat melalui **Bulk Redirects** atau Redirect Rules.
6. Aktifkan opsi mempertahankan *query string*, mencocokkan subpath, dan mempertahankan sisa path agar tautan menuju bagian situs tidak rusak.
7. Setelah domain utama aktif, arahkan `<nama-proyek>.pages.dev` ke domain utama jika Anda ingin mencegah dua alamat publik menampilkan konten yang sama.
8. Ulangi pemeriksaan canonical dan pastikan nilainya sama dengan alamat yang terlihat setelah seluruh pengalihan selesai.

Contoh hasil akhir yang benar:

```text
http://www.domainanda.com/...  →  https://domainanda.com/...
https://www.domainanda.com/... →  https://domainanda.com/...
https://proyek.pages.dev/...    →  https://domainanda.com/...
```

### I. Aktifkan FormSubmit

Gunakan data pengujian yang jelas, misalnya nama `Uji Formulir Website`, email Anda sendiri, dan keterangan bahwa pesan boleh diabaikan.

1. Buka formulir melalui domain publik, bukan melalui `file://` atau localhost.
2. Isi semua kolom wajib dan centang persetujuan.
3. Pilih salah satu layanan lalu kirim.
4. Pada penggunaan pertama, FormSubmit dapat mengirim email aktivasi ke `arifpramarta@gmail.com`.
5. Periksa Kotak Masuk, Spam, Promosi, dan Semua Email.
6. Buka email tersebut dan pilih tautan konfirmasi.
7. Kembali ke situs, muat ulang halaman, lalu kirim pengujian kedua.
8. Pastikan halaman menampilkan pesan berhasil hanya setelah layanan memberi konfirmasi.
9. Pastikan email kedua benar-benar diterima dan memuat nama, email, organisasi, jenis layanan, serta ringkasan kebutuhan.
10. Tekan **Reply/Balas** pada email yang diterima dan pastikan penerima mengarah ke alamat pengirim yang dimasukkan pada formulir.
11. Uji satu kali dengan jaringan terputus atau pemblokiran endpoint untuk memastikan pilihan Gmail dan salin ringkasan tetap tersedia.
12. Jika FormSubmit memberikan endpoint pengganti yang tidak menampilkan alamat email, masukkan endpoint tersebut pada `action` dan `data-form-endpoint`, lalu deploy ulang dan ulangi pengujian.

FormSubmit menyimpan kiriman untuk jangka waktu tertentu menurut kebijakan layanannya. Karena itu, jangan memasukkan data klien sensitif pada pengujian.

### J. Uji pratinjau ketika tautan dibagikan

1. Buka URL gambar sosial secara langsung dan pastikan gambar tampil.
2. Bagikan URL halaman utama melalui percakapan pribadi atau alat pemeriksa pratinjau.
3. Pastikan nama, deskripsi, dan gambar yang muncul sesuai.
4. Jika gambar lama masih muncul, tunggu cache platform atau gunakan alat penyegaran pratinjau dari platform terkait.
5. Jangan mengubah tautan profil LinkedIn. Pengaturan `og:image` hanya mengatur kartu pratinjau saat URL website dibagikan.

### K. Daftarkan ke Google Search Console

1. Buka Google Search Console dan tambahkan **Domain property** jika Anda dapat mengubah DNS. Properti ini mencakup HTTP, HTTPS, `www`, dan subdomain.
2. Salin record TXT verifikasi yang diberikan Google ke DNS domain.
3. Tunggu record terbaca, lalu selesaikan verifikasi.
4. Buka `https://domainanda.com/robots.txt` dan pastikan alamat sitemap benar.
5. Buka `https://domainanda.com/sitemap.xml` dan pastikan file XML tampil tanpa 404.
6. Pada Search Console, masuk ke laporan **Sitemaps**.
7. Masukkan `sitemap.xml`, kemudian pilih **Submit**.
8. Pastikan status akhirnya **Success**. Jika gagal, buka detail kesalahan sebelum mengirim ulang.
9. Gunakan **URL Inspection** untuk halaman utama.
10. Jalankan pemeriksaan URL langsung dan pilih **Request indexing** jika halaman dapat diakses Google.

Pengindeksan tidak terjadi seketika dan permintaan pengindeksan tidak menjamin halaman langsung muncul di hasil pencarian.

### L. Simpan bukti dan siapkan pemulihan

1. Simpan ZIP yang sudah dipublikasikan dengan nomor versi dan tanggal.
2. Simpan tangkapan layar halaman utama desktop dan ponsel.
3. Catat domain utama, registrar, akun Cloudflare, nama proyek Pages, dan tanggal publikasi pada tempat yang aman.
4. Jangan menyimpan kata sandi atau token di folder proyek.
5. Jika versi baru bermasalah, buka **Deployments** pada proyek Pages.
6. Cari deployment produksi terakhir yang masih baik, buka menu tiga titik, lalu pilih **Rollback to this deployment**.
7. Setelah rollback, uji kembali halaman utama dan formulir.
8. Perbaiki folder lokal terlebih dahulu sebelum mengunggah versi berikutnya.

## Pembagian pekerjaan yang praktis

### Informasi dari Anda

- domain final;
- pilihan alamat utama dengan atau tanpa `www`;
- akses ke panel domain/DNS;
- akses ke akun Cloudflare;
- akses ke email penerima FormSubmit.

### Pekerjaan yang dapat saya selesaikan dari folder

- mengganti seluruh placeholder domain;
- memperbarui canonical, Open Graph, robots, dan sitemap;
- membuat folder atau ZIP publikasi yang bersih;
- menjalankan pengujian lokal terakhir;
- memeriksa struktur dan isi paket;
- mendampingi atau menjalankan langkah pada dasbor hosting ketika diminta;
- menguji situs publik setelah domain aktif.

### Tindakan yang tetap memerlukan Anda

- membeli domain atau menyetujui biaya layanan;
- masuk ke akun yang memerlukan kredensial pribadi;
- mengonfirmasi email aktivasi FormSubmit;
- memberikan keputusan akhir tentang alamat utama situs.

## Lampiran: checklist untuk hosting selain Cloudflare

Gunakan bagian ini jika Anda memilih penyedia hosting statis lain. Prinsip dan urutan kerjanya sama, sedangkan nama menu pada dasbor dapat berbeda.

### 1. Tentukan alamat dan tempat hosting

- Tentukan domain final, misalnya `namaanda.com` atau `www.namaanda.com`.
- Tentukan layanan hosting statis yang akan digunakan.
- Tentukan satu alamat utama: memakai `www` atau tanpa `www`. Alamat lainnya diarahkan ke alamat utama.

Jangan mengubah metadata domain sebelum alamat final diputuskan agar tidak perlu mengulang pekerjaan.

### 2. Siapkan berkas publikasi

Pertahankan nama, kapitalisasi, dan susunan folder berikut:

```text
index.html
404.html
robots.txt
sitemap.xml
Aset/
  apple-touch-icon-transparent.png
  favicon-transparent-32.png
  client-logos.css
  client-logos.js
  landing.css
  hero-data-scene.css
  hero-data-scene.js
  social-preview-mohamad-arif-pramarta.jpg
Foto/
  portrait-semi-formal-640.webp
  portrait-semi-formal-960.webp
  portrait-semi-formal-960.jpg
Logo Klien/
  web/
    bappenas.webp
    bright-sinergi-global.webp
    icg.webp
    indekstat.webp
```

Jangan unggah berkas dan folder kerja berikut:

- `PRD_Landing_Page_Jasa_Mohamad_Arif_Pramarta_v2.docx`
- `build_prd_landing_page.py`
- `_cv_policy_ai_work/`, `_prd_render/`, `Portofolio/`, dan `testimonial-react/`
- `tmp/`, `.codex-backups/`, `.claude/`, `.vite/`, dan `release/`
- PNG asli di bagian utama folder `Logo Klien/`
- `Foto/portrait-semi-formal-full.jpg` (foto sumber resolusi penuh)

### Pembersihan folder — 17 September 2026

Berkas berikut dipindahkan ke Recycle Bin karena sudah tidak dipakai (dapat dipulihkan dari Recycle Bin bila diperlukan):

- `preview-testimoni-grid.html` dan `Hero_Landing_Page_Mohamad_Arif_Pramarta.html`
- Paket lama: `release/landing-page-preview-2026-09-16.zip`, `release/preview-2026-09-16T10-27-14-613Z/`, dan folder pratinjau 17 September sebelum pemisahan CSS
- Aset tidak terpakai: `web-icon-transparent.png`, `hero-title-fit.js`, `apple-touch-icon.png`, `favicon-32.png`, `hero-data-3d-160.webp`, `hero-data-3d-320.webp`
- Berkas sementara: `tmp/landing-audit/`, `tmp/landing-audit-after/`, `tmp/landing-before/`, dan cache `.vite/`

Sengaja dipertahankan: `tmp/pdfs/` (render halaman dokumen kajian), PRD, CV/portofolio, `testimonial-react/`, `.codex-backups/`, foto sumber resolusi penuh, dan PNG sumber logo.

### 3. Masukkan domain final

Setelah domain diputuskan:

1. Aktifkan `canonical` dan `og:url` pada `index.html`, lalu isi dengan URL utama situs.
2. Ubah `og:image` dan `twitter:image` menjadi URL absolut menuju gambar sosial, misalnya `https://domain-final.com/Aset/social-preview-mohamad-arif-pramarta.jpg`.
3. Ganti `DOMAIN-ANDA.com` pada `robots.txt` dan `sitemap.xml`.
4. Perbarui `lastmod` pada `sitemap.xml` dengan tanggal publikasi.
5. Simpan perubahan hanya di `index.html` (tidak ada lagi salinan HTML kedua).

Gambar Open Graph tersebut dipakai ketika tautan website dibagikan melalui LinkedIn, WhatsApp, dan platform lain. Ini tidak berkaitan dengan tautan profil LinkedIn di halaman.

### 4. Jalankan pemeriksaan lokal terakhir

Periksa melalui server lokal, bukan hanya dengan membuka `file://`:

- halaman utama terbuka tanpa gambar hilang;
- navigasi desktop dan ponsel bekerja;
- tab layanan dan carousel testimoni bekerja;
- semua tombol menuju bagian atau situs yang tepat;
- tidak ada halaman yang melebar pada layar ponsel;
- formulir memvalidasi kolom wajib;
- teks, harga, nama, jabatan, dan testimoni sudah final;
- tidak ada lagi `DOMAIN-ANDA.com` pada paket publikasi.

### 5. Unggah ke hosting

1. Buat proyek situs statis pada layanan hosting yang dipilih.
2. Unggah isi paket publikasi ke direktori akar situs. `index.html` harus berada langsung di akar, bukan di dalam folder tambahan.
3. Tidak ada proses build dan tidak ada perintah instalasi. Jika layanan meminta *build command*, biarkan kosong.
4. Jika layanan meminta *publish directory*, pilih direktori yang langsung berisi `index.html`.
5. Lakukan publikasi pertama menggunakan alamat sementara dari layanan hosting.

### 6. Hubungkan domain dan HTTPS

1. Tambahkan domain final pada pengaturan hosting.
2. Pasang catatan DNS yang diberikan layanan hosting pada pengelola domain.
3. Tunggu sampai status domain aktif.
4. Pastikan sertifikat HTTPS aktif dan `http://` otomatis diarahkan ke `https://`.
5. Pastikan versi `www` dan tanpa `www` tidak membuka dua situs terpisah; salah satunya harus mengarah ke alamat utama.

### 7. Aktifkan dan uji formulir

Lakukan setelah situs sudah bisa dibuka melalui domain atau alamat hosting publik:

1. Isi formulir dengan data pengujian yang mudah dikenali.
2. Kirim formulir satu kali.
3. Buka email aktivasi dari FormSubmit yang masuk ke `arifpramarta@gmail.com`, lalu konfirmasi alamat tersebut.
4. Jika email tidak terlihat, periksa folder Spam, Promosi, dan Semua Email.
5. Kirim formulir sekali lagi setelah aktivasi.
6. Pastikan pesan sampai, subjek menyebut jenis layanan, isi data lengkap, dan tombol balas mengarah ke email calon klien.
7. Uji juga kondisi gagal untuk memastikan pilihan “Buka Gmail” dan “Salin Ringkasan” muncul.
8. Setelah endpoint acak FormSubmit tersedia, ganti alamat email terbuka pada `action` dan `data-form-endpoint` dengan endpoint tersebut.

### 8. Periksa situs yang sudah tayang

- Buka halaman di desktop, Android, serta Safari/iPhone bila tersedia.
- Periksa hero, foto, logo klien, pengalaman, layanan, testimoni, harga, FAQ, dan formulir.
- Buka tautan LinkedIn, Tableau, dan Superprof.
- Bagikan URL situs untuk memeriksa judul, deskripsi, dan gambar pratinjau.
- Buka `/robots.txt` dan `/sitemap.xml` dari domain publik.
- Pastikan halaman galat 404 tidak menggantikan aset yang namanya mengandung spasi, khususnya folder `Logo Klien`.

### 9. Daftarkan ke mesin pencari

Setelah seluruh pemeriksaan lolos:

1. Tambahkan domain ke Google Search Console.
2. Verifikasi kepemilikan domain sesuai metode yang tersedia.
3. Kirim URL `https://domain-final.com/sitemap.xml`.
4. Minta pengindeksan untuk halaman utama.

### 10. Simpan versi final

- Simpan salinan paket yang benar-benar dipublikasikan.
- Catat domain, layanan hosting, dan tanggal publikasi.
- Setiap kali isi diperbarui, sinkronkan kedua HTML, perbarui tanggal sitemap bila relevan, jalankan pengujian, lalu publikasikan versi baru.

## Status saat ini (17 September 2026)

- `index.html` (satu-satunya berkas HTML kerja), `404.html`, dan aset web sudah tersedia. Tampilan utama kini berada di `Aset/landing.css`.
- Tampilan responsif, formulir (termasuk kolom WhatsApp), testimoni 3 kartu, dan halaman 404 sudah diuji secara lokal pada lebar 390 dan 1440 piksel.
- Paket pratinjau terbaru: `release/landing-page-preview-2026-09-17.zip`.
- Cadangan sebelum tiap perubahan tersimpan di `.codex-backups/` (awalan `before-...-2026-09-16`).
- Menunggu tahap deploy: domain final, metadata berbasis domain, aktivasi FormSubmit, pengiriman email nyata, HTTPS, aktivasi Cloudflare Web Analytics, dan pemeriksaan di perangkat nyata.
