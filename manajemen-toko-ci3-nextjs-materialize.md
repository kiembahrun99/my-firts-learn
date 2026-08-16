# Spesifikasi Project — Manajemen Toko
## Backend CodeIgniter 3 + SQLite + REST API + Next.js + Materialize CSS CDN

---

# 1. Tujuan

Bangun aplikasi web **Manajemen Toko** dengan arsitektur frontend dan backend terpisah.

Tujuan utama:

- ringan
- smooth
- mudah digunakan
- mudah dikembangkan
- mudah di-maintain
- backend dapat digunakan oleh frontend lain di masa depan
- tidak bergantung pada database service seperti MySQL/PostgreSQL untuk versi pertama

## Modul Versi 1

1. Dashboard
2. Barang
3. Distributor
4. Barang Distributor
5. Pesanan
6. Retur

## Jangan implementasikan dulu

- Login
- Admin/Pegawai
- Role/permission
- User management
- Stok
- Mutasi stok
- POS/Kasir
- Penjualan
- Pembayaran
- Akuntansi
- Laporan keuangan
- Multi toko
- WhatsApp API
- Payment gateway
- Cloud storage

Arsitektur harus tetap memungkinkan fitur-fitur tersebut ditambahkan pada fase berikutnya.

---

# 2. Arsitektur

Gunakan arsitektur:

```text
                    ┌─────────────────────────┐
                    │       Next.js           │
                    │       Frontend          │
                    │                         │
                    │ Materialize CSS via CDN │
                    │ Fetch API               │
                    └────────────┬────────────┘
                                 │
                              HTTP/JSON
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │     CodeIgniter 3       │
                    │       REST API          │
                    │                         │
                    │ Controllers              │
                    │ Models                   │
                    │ Validation               │
                    │ Upload handling          │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │         SQLite          │
                    │       Database          │
                    └─────────────────────────┘
```

## Aturan penting

Frontend **tidak boleh** mengakses SQLite secara langsung.

Frontend hanya berkomunikasi dengan backend melalui REST API.

Backend menjadi satu-satunya pihak yang berkomunikasi dengan database.

---

# 3. Backend

Gunakan:

- CodeIgniter 3
- PHP
- SQLite
- REST API
- JSON response

CodeIgniter 3 harus digunakan sebagai backend API-only.

Jangan membuat HTML UI utama pada CodeIgniter.

Backend bertanggung jawab atas:

- database
- CRUD
- validation
- business logic
- upload foto
- response JSON
- error handling
- database integrity

---

# 4. Frontend

Gunakan:

- Next.js
- React
- TypeScript jika project mendukung
- Materialize CSS versi terbaru yang tersedia dan stabil melalui CDN
- Fetch API

Frontend bertanggung jawab atas:

- UI
- UX
- routing halaman
- form
- tabel
- modal
- loading
- error state
- success notification
- komunikasi API

Jangan membuat API/database logic di frontend.

---

# 5. Materialize CSS

Gunakan Materialize CSS melalui CDN.

Jangan menginstall Materialize melalui npm jika tujuan project adalah penggunaan CDN.

Gunakan versi stabil terbaru yang tersedia pada saat implementasi.

Pastikan:

- CSS Materialize termuat
- JavaScript Materialize termuat
- komponen Materialize berfungsi
- sidenav berfungsi
- modal berfungsi
- select berfungsi
- toast berfungsi
- dropdown berfungsi

Gunakan Materialize sebagai UI foundation.

Custom CSS boleh digunakan untuk:

- branding
- spacing khusus
- dashboard
- responsive behavior
- glass/frosted effect
- komponen yang tidak tersedia di Materialize

Jangan membuat UI terlalu berat.

---

# 6. Design UI

Gunakan konsep:

**Modern Material Dashboard + Clean UI + Soft/Frosted Glass**

Prioritas:

1. Usability
2. Performance
3. Readability
4. Responsive
5. Visual consistency

Jangan menggunakan animasi berlebihan.

Gunakan:

- sidenav
- navbar
- cards
- tables
- modals
- badges/chips
- buttons
- forms
- dropdown
- toast
- pagination
- responsive grid

---

# 7. Struktur Frontend

Contoh:

```text
frontend/
├── app/
│   ├── page.tsx
│   ├── barang/
│   │   ├── page.tsx
│   │   ├── tambah/
│   │   └── [id]/
│   ├── distributor/
│   │   ├── page.tsx
│   │   ├── tambah/
│   │   └── [id]/
│   ├── pesanan/
│   │   ├── page.tsx
│   │   ├── tambah/
│   │   └── [id]/
│   └── retur/
│       ├── page.tsx
│       ├── tambah/
│       └── [id]/
│
├── components/
│   ├── layout/
│   ├── ui/
│   ├── barang/
│   ├── distributor/
│   ├── pesanan/
│   └── retur/
│
├── lib/
│   ├── api.ts
│   ├── format.ts
│   └── constants.ts
│
└── public/
```

Sesuaikan dengan struktur Next.js yang digunakan project.

Jika project existing sudah memiliki struktur yang berbeda tetapi rapi, jangan melakukan rewrite tanpa alasan.

---

# 8. Struktur Backend

Contoh:

```text
backend/
├── application/
│   ├── controllers/
│   │   └── api/
│   │       ├── Barang.php
│   │       ├── Distributor.php
│   │       ├── BarangDistributor.php
│   │       ├── Pesanan.php
│   │       └── Retur.php
│   │
│   ├── models/
│   │   ├── Barang_model.php
│   │   ├── Distributor_model.php
│   │   ├── BarangDistributor_model.php
│   │   ├── Pesanan_model.php
│   │   ├── DetailPesanan_model.php
│   │   └── Retur_model.php
│   │
│   ├── libraries/
│   └── helpers/
│
├── uploads/
│   ├── barang/
│   ├── distributor/
│   └── retur/
│
└── database/
    └── toko.sqlite
```

Struktur dapat disesuaikan dengan project CI3 existing.

---

# 9. Database

Gunakan SQLite.

Contoh:

```text
backend/database/toko.sqlite
```

Jangan menyimpan database SQLite di folder public/web-accessible.

Gunakan konfigurasi CodeIgniter agar database berada di lokasi yang aman.

---

# 10. Database Schema

## 10.1 Barang

Table:

```text
barang
```

Field:

```text
id
barcode
nama
harga_beli
harga_jual
foto
keterangan
status
created_at
updated_at
```

Aturan:

- `id` primary key
- `barcode` unique jika diisi
- `nama` wajib
- `harga_beli >= 0`
- `harga_jual >= 0`
- `status`: `AKTIF` / `NONAKTIF`

Jangan menyimpan `id_distributor` langsung pada tabel barang.

Karena satu barang dapat berasal dari beberapa distributor.

---

# 11. Distributor

Table:

```text
distributor
```

Field:

```text
id
nama_distributor
nama_sales
no_wa_sales
no_wa_distributor
interval_kunjungan
hari_kunjungan
foto
keterangan
status
created_at
updated_at
```

## interval_kunjungan

Gunakan angka:

```text
1 = setiap 1 minggu
2 = setiap 2 minggu
```

Jangan menyimpan:

```text
"1 minggu sekali"
"2 minggu sekali"
```

## hari_kunjungan

Gunakan:

```text
SENIN
SELASA
RABU
KAMIS
JUMAT
SABTU
```

---

# 12. Barang Distributor

Table:

```text
barang_distributor
```

Field:

```text
id
barang_id
distributor_id
harga_beli
keterangan
created_at
updated_at
```

Relasi:

```text
barang_distributor.barang_id
    -> barang.id

barang_distributor.distributor_id
    -> distributor.id
```

Tambahkan unique constraint:

```text
barang_id + distributor_id
```

## Alasan

Harga beli dapat berbeda antara distributor.

Contoh:

```text
Indomie
Distributor A = 110.000
Distributor B = 108.000
```

---

# 13. Pesanan

Gunakan header-detail.

Table:

```text
pesanan
```

Field:

```text
id
distributor_id
tanggal_pesanan
status
keterangan
created_at
updated_at
```

Status:

```text
DRAFT
DIPESAN
DIPROSES
SELESAI
DIBATALKAN
```

---

# 14. Detail Pesanan

Table:

```text
detail_pesanan
```

Field:

```text
id
pesanan_id
barang_id
jumlah
harga_beli
subtotal
```

Relasi:

```text
detail_pesanan.pesanan_id
    -> pesanan.id

detail_pesanan.barang_id
    -> barang.id
```

Perhitungan:

```text
subtotal = jumlah × harga_beli
```

Simpan `harga_beli` pada detail pesanan.

Tujuannya agar histori harga tetap benar meskipun harga barang berubah di kemudian hari.

---

# 15. Retur

Table:

```text
retur
```

Field:

```text
id
barang_id
distributor_id
jumlah_retur
alasan_retur
foto
keterangan
status
tanggal_retur
created_at
updated_at
```

Status:

```text
DIAJUKAN
DITERIMA
DITOLAK
SELESAI
```

Relasi:

```text
retur.barang_id
    -> barang.id

retur.distributor_id
    -> distributor.id
```

Jangan menyimpan `nama_barang` di tabel retur.

Nama barang diambil melalui relasi.

---

# 16. Relasi Database

```text
                    ┌───────────────┐
                    │  Distributor  │
                    └───────┬───────┘
                            │
                ┌───────────┼─────────────┐
                │           │             │
                ▼           ▼             ▼
       BarangDistributor  Pesanan       Retur
                │           │             │
                ▼           ▼             ▼
             Barang   DetailPesanan     Barang
                           │
                           ▼
                         Barang
```

---

# 17. ID

Gunakan ID integer auto increment atau UUID/CUID sesuai kebutuhan project.

Untuk CI3 + SQLite, integer primary key auto increment diperbolehkan dan merupakan pilihan sederhana.

Jika menggunakan integer ID:

- jangan expose informasi sensitif
- endpoint tetap harus melakukan validasi akses/data
- gunakan ID hanya sebagai identifier teknis

---

# 18. REST API

Gunakan endpoint konsisten.

Base URL contoh:

```text
/api
```

## Barang

```text
GET    /api/barang
POST   /api/barang
GET    /api/barang/{id}
PUT    /api/barang/{id}
DELETE /api/barang/{id}
```

## Distributor

```text
GET    /api/distributor
POST   /api/distributor
GET    /api/distributor/{id}
PUT    /api/distributor/{id}
DELETE /api/distributor/{id}
```

## Barang Distributor

```text
GET    /api/barang-distributor
POST   /api/barang-distributor
GET    /api/barang-distributor/{id}
PUT    /api/barang-distributor/{id}
DELETE /api/barang-distributor/{id}
```

## Pesanan

```text
GET    /api/pesanan
POST   /api/pesanan
GET    /api/pesanan/{id}
PUT    /api/pesanan/{id}
DELETE /api/pesanan/{id}
```

## Retur

```text
GET    /api/retur
POST   /api/retur
GET    /api/retur/{id}
PUT    /api/retur/{id}
DELETE /api/retur/{id}
```

---

# 19. API Response

Gunakan response JSON konsisten.

Success:

```json
{
  "success": true,
  "message": "Data berhasil disimpan",
  "data": {}
}
```

List:

```json
{
  "success": true,
  "data": [],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 100,
    "total_pages": 5
  }
}
```

Error:

```json
{
  "success": false,
  "message": "Data tidak ditemukan",
  "errors": {}
}
```

Gunakan HTTP status code yang sesuai:

```text
200 OK
201 Created
400 Bad Request
404 Not Found
422 Unprocessable Entity
500 Internal Server Error
```

---

# 20. API CORS

Karena frontend dan backend dapat berjalan pada origin berbeda, backend harus menyediakan konfigurasi CORS yang benar.

Untuk development, izinkan origin frontend development.

Contoh:

```text
http://localhost:3000
```

Untuk production, gunakan origin frontend production yang sebenarnya.

Jangan menggunakan wildcard CORS secara permanen jika nantinya aplikasi memiliki authentication.

---

# 21. Frontend API Client

Buat satu helper API.

Contoh konsep:

```text
lib/api.ts
```

Semua request frontend sebaiknya melalui helper tersebut.

Contoh:

```text
api.get()
api.post()
api.put()
api.delete()
```

Jangan mengulang logic fetch yang sama di setiap halaman.

---

# 22. Environment Frontend

Gunakan environment variable untuk API URL.

Contoh:

```env
NEXT_PUBLIC_API_URL=http://localhost/backend/index.php/api
```

Production:

```env
NEXT_PUBLIC_API_URL=https://domain.com/api
```

Jangan hardcode URL backend di banyak file.

---

# 23. Barang — UI

## List Barang

Tampilkan:

- Foto
- Barcode
- Nama
- Harga beli
- Harga jual
- Distributor
- Status
- Action

Fitur:

- search
- filter status
- sort
- pagination
- tambah
- edit
- detail
- nonaktifkan

## Form

Field:

- barcode
- nama barang
- harga beli
- harga jual
- distributor
- foto
- keterangan
- status

---

# 24. Distributor — UI

## List

Tampilkan:

- foto
- nama distributor
- nama sales
- WhatsApp sales
- WhatsApp distributor
- jadwal kunjungan
- status
- action

Contoh:

```text
Setiap 1 minggu
Senin
```

atau:

```text
Setiap 2 minggu
Kamis
```

## Form

Field:

- nama distributor
- nama sales
- no WA sales
- no WA distributor
- interval kunjungan
- hari kunjungan
- foto
- keterangan
- status

---

# 25. Pesanan — UI

Pesanan harus mendukung banyak barang.

Flow:

```text
1. Pilih distributor
2. Tambah barang
3. Masukkan jumlah
4. Ambil harga beli
5. Hitung subtotal
6. Tambah barang lain jika diperlukan
7. Hitung total
8. Simpan
```

Contoh:

```text
Pesanan #001
Distributor: ABC

Barang             Jumlah    Harga       Subtotal
---------------------------------------------------
Indomie              2       110.000      220.000
Aqua                 3        45.000      135.000
Kopi ABC             1        80.000       80.000
---------------------------------------------------
Total                                      435.000
```

---

# 26. Retur — UI

Tampilkan:

- ID retur
- barang
- distributor
- jumlah
- alasan
- tanggal
- status
- action

Form:

- barang
- distributor
- jumlah
- alasan retur
- foto
- keterangan
- tanggal
- status

---

# 27. Dashboard

Dashboard harus mengambil data aktual dari API.

Card:

```text
Total Barang
Total Distributor
Total Pesanan
Total Retur
```

Tampilkan:

- pesanan terbaru
- retur terbaru
- jadwal kunjungan distributor
- aktivitas terbaru jika memungkinkan

Jangan hardcode angka dashboard.

---

# 28. Search & Pagination

Implementasikan server-side pagination untuk endpoint list.

Contoh:

```text
GET /api/barang?page=1&per_page=20
```

Search:

```text
GET /api/barang?search=indomie
```

Filter:

```text
GET /api/barang?status=AKTIF
```

Gabungan:

```text
GET /api/barang?search=indomie&status=AKTIF&page=1&per_page=20
```

Backend harus melakukan filtering/pagination melalui query database.

Jangan mengambil seluruh tabel lalu filtering di browser jika data berpotensi besar.

---

# 29. Upload Foto

Upload ditangani oleh backend CodeIgniter.

Folder:

```text
uploads/
├── barang/
├── distributor/
└── retur/
```

Frontend menggunakan:

```text
multipart/form-data
```

Backend harus:

- memvalidasi MIME
- memvalidasi extension
- membatasi ukuran
- membuat nama file unik
- tidak mempercayai filename user
- menyimpan path relatif
- menghapus file lama ketika foto diganti jika aman dilakukan

Jangan menyimpan binary image di SQLite.

---

# 30. Validasi Barang

Backend wajib memvalidasi:

- nama wajib
- harga beli angka
- harga jual angka
- harga >= 0
- barcode unique jika diisi
- status valid
- foto valid jika ada

Frontend boleh melakukan validasi tambahan untuk UX.

Server-side validation tetap wajib.

---

# 31. Validasi Distributor

Validasi:

- nama distributor wajib
- interval hanya `1` atau `2`
- hari harus salah satu dari SENIN-SABTU
- status valid
- nomor WhatsApp tidak kosong jika memang diwajibkan oleh UI

Jangan melakukan regex nomor WhatsApp terlalu ketat.

---

# 32. Validasi Pesanan

Validasi:

- distributor valid
- minimal satu detail
- barang valid
- jumlah > 0
- harga valid
- subtotal dihitung backend

Jangan mempercayai subtotal yang dikirim frontend.

Backend harus menghitung ulang:

```text
subtotal = jumlah × harga_beli
```

Dan total juga dihitung backend.

---

# 33. Validasi Retur

Validasi:

- barang valid
- distributor valid
- jumlah > 0
- alasan jika diwajibkan
- status valid
- tanggal valid
- foto valid jika ada

---

# 34. Transaksi Database

Saat membuat pesanan:

```text
BEGIN TRANSACTION

1. insert pesanan
2. insert detail pesanan
3. hitung subtotal
4. hitung total
5. COMMIT
```

Jika salah satu proses gagal:

```text
ROLLBACK
```

Jangan menghasilkan pesanan setengah jadi.

Gunakan transaction database CodeIgniter.

---

# 35. Delete Strategy

Jangan sembarangan hard delete data yang sudah memiliki histori.

## Barang

Jika sudah digunakan:

```text
status = NONAKTIF
```

## Distributor

Jika sudah memiliki histori:

```text
status = NONAKTIF
```

## Pesanan

Hard delete hanya jika masih:

```text
DRAFT
```

Untuk pesanan yang sudah diproses, hindari penghapusan permanen.

## Retur

Jangan menghapus histori retur secara sembarangan.

---

# 36. Format Rupiah

Database menyimpan angka:

```text
12500
```

Frontend menampilkan:

```text
Rp 12.500
```

Jangan menyimpan:

```text
"Rp 12.500"
```

di database.

Buat helper frontend:

```text
formatRupiah()
```

---

# 37. Format Tanggal

Database:

```text
YYYY-MM-DD HH:mm:ss
```

UI Indonesia:

```text
16 Agustus 2026
```

Timestamp:

```text
16 Agu 2026, 14:30
```

Perhatikan timezone WIB pada frontend/backend.

---

# 38. Loading State

Semua request API harus memiliki state:

```text
loading
success
error
empty
```

Contoh:

```text
Memuat data...
```

Saat gagal:

```text
Gagal memuat data.
[ Coba Lagi ]
```

---

# 39. Toast

Gunakan Materialize toast untuk:

- berhasil tambah
- berhasil edit
- berhasil hapus/nonaktif
- berhasil update status
- error API

Contoh:

```text
Barang berhasil ditambahkan
```

---

# 40. Empty State

Jika data kosong:

```text
Belum ada barang.

[ + Tambah Barang ]
```

Jangan menampilkan tabel kosong tanpa informasi.

---

# 41. Responsive

Harus nyaman digunakan pada:

- desktop
- laptop
- tablet
- smartphone

Pada mobile:

- sidenav menjadi drawer
- tabel dapat horizontal scroll
- form menjadi satu kolom
- tombol action mudah ditekan
- modal tidak keluar layar

---

# 42. Security Basic

Walaupun belum ada login:

Backend harus:

- validasi semua input
- validasi upload
- membatasi file upload
- menggunakan query parameterized
- tidak membocorkan stack trace
- tidak membocorkan path server
- tidak mempercayai data frontend
- menggunakan HTTP status code yang tepat

Jangan menggunakan raw SQL jika query builder CodeIgniter sudah cukup.

Jika raw SQL benar-benar diperlukan, parameter harus dibinding.

---

# 43. Logging

Backend harus memiliki logging yang cukup untuk debugging tetapi jangan memasukkan:

- password
- token
- data sensitif
- file content

Production tidak boleh menampilkan error PHP/SQL mentah kepada user.

---

# 44. Development Workflow

Sebelum mengubah project existing:

1. Inspect struktur project.
2. Identifikasi versi PHP.
3. Identifikasi versi CodeIgniter.
4. Identifikasi database existing.
5. Identifikasi package manager frontend.
6. Identifikasi versi Next.js.
7. Jangan overwrite kode existing tanpa alasan.
8. Pertahankan fitur yang masih relevan.

Kemudian:

```text
1. Setup SQLite
2. Buat schema database
3. Buat model CI3
4. Buat REST API
5. Test API
6. Setup Next.js
7. Setup Materialize CDN
8. Buat layout
9. Buat Barang
10. Buat Distributor
11. Buat BarangDistributor
12. Buat Pesanan
13. Buat Retur
14. Buat Dashboard
15. Upload foto
16. Search/filter/pagination
17. Validation
18. Error handling
19. Responsive UI
20. Testing
21. Final cleanup
```

---

# 45. Testing API

Test minimal:

## Barang

```text
GET
POST
GET detail
PUT
DELETE/nonaktif
```

## Distributor

```text
GET
POST
GET detail
PUT
DELETE/nonaktif
```

## Barang Distributor

```text
GET
POST
PUT
DELETE
```

## Pesanan

```text
GET
POST multi-detail
GET detail
PUT
DELETE draft
```

## Retur

```text
GET
POST
GET detail
PUT
DELETE
```

Test juga:

- invalid ID
- missing field
- harga negatif
- jumlah 0
- barcode duplicate
- upload file invalid
- distributor tidak ditemukan
- barang tidak ditemukan

---

# 46. Testing Frontend

Pastikan:

- halaman dapat dibuka
- API URL benar
- data list tampil
- form submit berhasil
- validation bekerja
- loading tampil
- error tampil
- toast tampil
- modal bekerja
- select Materialize bekerja
- pagination bekerja
- search bekerja
- upload foto bekerja
- responsive bekerja

---

# 47. Seed / Sample Data

Buat data dummy untuk development.

Contoh:

### Distributor

```text
Distributor ABC
Distributor XYZ
Distributor Maju
```

### Barang

```text
Indomie Goreng
Aqua 600ml
Kopi ABC
```

Gunakan data dummy.

Jangan menggunakan data pribadi/nyata.

---

# 48. Dokumentasi

Buat README yang menjelaskan:

## Backend

```text
requirements
installation
configuration
database
SQLite
API endpoint
upload
CORS
```

## Frontend

```text
requirements
installation
API URL
Materialize CDN
development
production
```

Contoh development:

```bash
npm install
npm run dev
```

Backend disesuaikan dengan environment PHP/Apache/Nginx yang digunakan.

---

# 49. Acceptance Criteria

Project dianggap selesai apabila:

- backend CI3 berjalan
- SQLite berjalan
- REST API berjalan
- frontend Next.js berjalan
- Materialize CDN berjalan
- frontend berhasil mengambil data API
- CRUD Barang berfungsi
- CRUD Distributor berfungsi
- BarangDistributor berfungsi
- Pesanan multi-item berfungsi
- Retur berfungsi
- upload foto berfungsi
- search berfungsi
- filter berfungsi
- pagination berfungsi
- validation berfungsi
- dashboard mengambil data aktual
- responsive desktop/mobile
- error handling berjalan
- database transaction untuk pesanan berjalan
- tidak ada error JavaScript yang tidak tertangani
- tidak ada error PHP yang tidak tertangani
- dokumentasi tersedia

---

# 50. Prinsip Maintenance

Prioritaskan:

- kode sederhana
- struktur jelas
- dependency minimum
- API konsisten
- database relation jelas
- reusable component
- validation terpusat
- error handling konsisten

Hindari:

- over-engineering
- dependency tidak perlu
- duplicate code
- query database berulang
- hardcoded API URL
- hardcoded dashboard data
- hardcoded status di banyak tempat

---

# 51. Instruksi Khusus Untuk AI Agent

Jangan hanya menjelaskan solusi.

**Kerjakan implementasinya langsung.**

Sebelum coding:

1. Inspect project.
2. Identifikasi file existing.
3. Identifikasi apakah frontend/backend sudah tersedia.
4. Identifikasi versi software.
5. Jangan merusak kode existing yang masih digunakan.

Jika project kosong:

Buat struktur project sesuai spesifikasi.

Jika project sudah ada:

Integrasikan ke project existing dengan perubahan seminimal mungkin.

## Backend

Implementasikan:

- database SQLite
- schema
- models
- controllers
- REST API
- validation
- upload
- CORS
- error handling
- transaction

## Frontend

Implementasikan:

- layout
- navigation
- dashboard
- CRUD Barang
- CRUD Distributor
- BarangDistributor
- Pesanan
- Retur
- search
- filter
- pagination
- modal
- toast
- loading
- empty state
- responsive design

---

# 52. Jangan Keluar Scope

Jangan menambahkan:

- authentication
- user management
- stok
- POS
- penjualan
- payment
- accounting

kecuali diminta secara eksplisit.

Jangan mengganti:

- CodeIgniter 3
- SQLite
- Next.js
- Materialize CDN

dengan teknologi lain tanpa instruksi.

---

# 53. Final Verification

Sebelum menyatakan pekerjaan selesai:

## Backend

Pastikan:

- tidak ada PHP syntax error
- tidak ada database error
- semua endpoint utama dapat dipanggil
- JSON response konsisten
- CORS benar
- upload bekerja
- transaction bekerja

## Frontend

Pastikan:

- tidak ada compile error
- tidak ada runtime error
- semua halaman dapat dibuka
- API berhasil dipanggil
- Materialize component terinisialisasi
- responsive
- loading/error/empty state tersedia

## Database

Pastikan:

- foreign key benar
- unique constraint benar
- tidak ada data duplikat yang tidak diinginkan
- migration/schema dapat dibuat ulang
- backup SQLite mudah dilakukan

---

# 54. Hasil Akhir yang Diharapkan

Hasil akhir harus berupa aplikasi:

```text
                MANAJEMEN TOKO
                       │
        ┌──────────────┼──────────────┐
        │              │              │
     Barang       Distributor       Pesanan
        │              │              │
        └────── BarangDistributor ────┘
                       │
                     Retur
```

Dengan:

```text
Frontend
Next.js + Materialize CDN
          │
          │ REST JSON
          ▼
Backend
CodeIgniter 3
          │
          ▼
SQLite
```

Aplikasi harus benar-benar runnable dan dapat digunakan, bukan sekadar prototype atau contoh kode.
