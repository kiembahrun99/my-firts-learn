# Spesifikasi Project — Manajemen Toko

## 1. Tujuan

Bangun aplikasi web **Manajemen Toko** yang ringan, smooth, modern, mudah digunakan, dan mudah di-maintain.

Versi pertama fokus pada:

1. Manajemen Barang
2. Manajemen Distributor
3. Manajemen Pesanan
4. Manajemen Retur
5. Dashboard ringkas

Jangan implementasikan fitur di luar scope tanpa alasan teknis yang kuat.

---

# 2. Tech Stack

Gunakan:

- **Next.js** versi stabil terbaru yang kompatibel dengan environment project
- **TypeScript**
- **SQLite**
- **Prisma ORM**
- **Bootstrap 5**
- CSS custom seperlunya untuk tampilan modern
- Next.js App Router

Prinsip:

- Jangan membuat backend terpisah.
- Gunakan Next.js untuk frontend dan backend/API.
- Jangan menggunakan MySQL/PostgreSQL untuk versi pertama.
- Jangan menambahkan Redis, Docker, atau service tambahan kecuali memang diperlukan oleh environment deployment.
- Database harus mudah di-backup karena SQLite berupa file database.

---

# 3. Scope Versi 1

## Wajib

### Barang
CRUD lengkap:

- Tambah barang
- Lihat daftar barang
- Detail barang
- Edit barang
- Hapus/nonaktifkan barang
- Pencarian
- Filter
- Pagination jika data banyak
- Upload foto

### Distributor
CRUD lengkap:

- Tambah distributor
- Lihat daftar distributor
- Detail distributor
- Edit distributor
- Hapus/nonaktifkan distributor
- Pencarian
- Filter
- Upload foto

### Pesanan
- Membuat pesanan
- Memilih distributor
- Menambahkan beberapa barang dalam satu pesanan
- Menentukan jumlah setiap barang
- Melihat detail pesanan
- Edit pesanan
- Mengubah status pesanan
- Menghapus pesanan
- Pencarian/filter

### Retur
- Membuat retur
- Memilih barang
- Menentukan jumlah retur
- Menentukan alasan retur
- Upload foto
- Status retur
- Melihat detail retur
- Edit
- Hapus
- Filter

### Dashboard
Tampilkan informasi ringkas:

- Total barang
- Total distributor
- Total pesanan
- Total retur
- Pesanan terbaru
- Retur terbaru
- Distributor yang memiliki jadwal kunjungan
- Ringkasan aktivitas terbaru jika memungkinkan

---

# 4. Fitur yang JANGAN dibuat dulu

Jangan implementasikan:

- Sistem login
- Admin/Pegawai
- Role & permission
- Manajemen user
- Stok
- Mutasi stok
- POS/Kasir
- Transaksi penjualan
- Pembayaran
- Laporan keuangan
- Akuntansi
- Multi-toko
- Integrasi WhatsApp API
- Integrasi payment gateway
- Cloud storage

Arsitektur harus tetap cukup rapi agar fitur tersebut dapat ditambahkan pada fase berikutnya.

---

# 5. Struktur Database

Gunakan Prisma Schema.

## 5.1 Barang

Model: `Barang`

Field:

- `id`
- `barcode`
- `nama`
- `hargaBeli`
- `hargaJual`
- `foto`
- `keterangan`
- `status`
- `createdAt`
- `updatedAt`

Relasi:

- satu barang dapat memiliki banyak distributor
- satu barang dapat muncul di banyak detail pesanan
- satu barang dapat memiliki banyak retur

### Catatan

Jangan simpan `idDistributor` langsung pada Barang.

Gunakan tabel relasi `BarangDistributor`.

Alasannya: satu barang dapat dibeli dari lebih dari satu distributor.

---

# 6. Distributor

Model: `Distributor`

Field:

- `id`
- `namaDistributor`
- `namaSales`
- `noWaSales`
- `noWaDistributor`
- `intervalKunjungan`
- `hariKunjungan`
- `foto`
- `keterangan`
- `status`
- `createdAt`
- `updatedAt`

### Aturan

`intervalKunjungan`:

- `1` = setiap 1 minggu
- `2` = setiap 2 minggu

`hariKunjungan`:

- SENIN
- SELASA
- RABU
- KAMIS
- JUMAT
- SABTU

Jangan menyimpan nilai seperti:

`"1 minggu sekali"`

atau

`"2 minggu sekali"`

di database.

Gunakan nilai terstruktur.

---

# 7. BarangDistributor

Model: `BarangDistributor`

Field:

- `id`
- `barangId`
- `distributorId`
- `hargaBeli`
- `keterangan`
- `createdAt`
- `updatedAt`

Relasi:

- `BarangDistributor` -> `Barang`
- `BarangDistributor` -> `Distributor`

Gunakan unique constraint pada:

`barangId + distributorId`

### Alasan harga beli

Harga beli dapat berbeda antara distributor A dan distributor B.

Harga default pada Barang tetap dapat digunakan sebagai harga umum/default.

---

# 8. Pesanan

Gunakan pola header-detail.

## 8.1 Pesanan

Model: `Pesanan`

Field:

- `id`
- `distributorId`
- `tanggalPesanan`
- `status`
- `keterangan`
- `createdAt`
- `updatedAt`

Relasi:

- satu Pesanan memiliki banyak DetailPesanan
- satu Pesanan dimiliki satu Distributor

Status:

- `DRAFT`
- `DIPESAN`
- `DIPROSES`
- `SELESAI`
- `DIBATALKAN`

---

# 9. DetailPesanan

Model: `DetailPesanan`

Field:

- `id`
- `pesananId`
- `barangId`
- `jumlah`
- `hargaBeli`
- `subtotal`

Relasi:

- `DetailPesanan` -> `Pesanan`
- `DetailPesanan` -> `Barang`

Hitung:

`subtotal = jumlah × hargaBeli`

Simpan `hargaBeli` pada detail pesanan agar histori harga tidak berubah ketika harga barang berubah di kemudian hari.

---

# 10. Retur

Model: `Retur`

Field:

- `id`
- `barangId`
- `distributorId`
- `jumlahRetur`
- `alasanRetur`
- `foto`
- `keterangan`
- `status`
- `tanggalRetur`
- `createdAt`
- `updatedAt`

Relasi:

- Retur -> Barang
- Retur -> Distributor

Status:

- `DIAJUKAN`
- `DITERIMA`
- `DITOLAK`
- `SELESAI`

---

# 11. ID Database

Gunakan ID internal yang aman dan mudah digunakan.

Prefer:

- UUID
- atau CUID

Jangan menggunakan ID integer auto-increment jika tidak ada alasan khusus.

ID internal tidak perlu ditampilkan sebagai identifier utama kepada pengguna.

Untuk UI, gunakan:

- barcode untuk barang
- nama barang
- nama distributor
- nomor pesanan yang readable jika diperlukan

---

# 12. Relasi Utama

Struktur relasi:

```text
Distributor
    │
    ├── BarangDistributor ── Barang
    │
    ├── Pesanan
    │       │
    │       └── DetailPesanan ── Barang
    │
    └── Retur ── Barang
```

---

# 13. Struktur Folder

Gunakan struktur Next.js App Router yang rapi.

Contoh:

```text
src/
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
│   ├── retur/
│   │   ├── page.tsx
│   │   ├── tambah/
│   │   └── [id]/
│   └── api/
│       ├── barang/
│       ├── distributor/
│       ├── pesanan/
│       └── retur/
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
│   ├── prisma.ts
│   ├── validations/
│   ├── utils/
│   └── constants/
│
└── types/
```

Sesuaikan struktur jika ada struktur project existing. Jangan menghancurkan kode existing yang masih digunakan.

---

# 14. UI/UX

Buat UI modern, bersih, responsif, dan cepat.

Gunakan konsep:

**Modern Dashboard / Frosted Glass / Soft UI**

Tetapi jangan berlebihan.

Prioritas:

1. Readability
2. Performance
3. Usability
4. Consistency
5. Visual design

Gunakan:

- sidebar desktop
- navbar/header
- card
- table
- modal
- offcanvas untuk mobile jika diperlukan
- badge status
- dropdown
- toast notification
- confirmation dialog

Gunakan Bootstrap 5 sebagai basis.

Custom CSS hanya untuk kebutuhan visual yang tidak tersedia di Bootstrap.

---

# 15. Layout

Desktop:

```text
┌──────────────────────────────────────────────────┐
│ Header                                            │
├──────────────┬───────────────────────────────────┤
│ Sidebar      │ Main Content                      │
│              │                                   │
│ Dashboard    │                                   │
│ Barang       │                                   │
│ Distributor  │                                   │
│ Pesanan      │                                   │
│ Retur        │                                   │
└──────────────┴───────────────────────────────────┘
```

Mobile:

- Sidebar menjadi offcanvas
- Table harus responsive
- Form harus nyaman digunakan dari smartphone
- Tombol action jangan terlalu kecil

---

# 16. Halaman Barang

## List

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

- Search berdasarkan nama/barcode
- Filter status
- Sort
- Pagination
- Tambah barang

## Form

Field:

- Barcode
- Nama barang
- Harga beli
- Harga jual
- Distributor
- Foto
- Keterangan
- Status

Validasi:

- nama wajib
- harga beli >= 0
- harga jual >= 0
- barcode jika diisi harus unik
- foto harus berupa file gambar yang valid

---

# 17. Halaman Distributor

## List

Tampilkan:

- Foto
- Nama distributor
- Sales
- WhatsApp sales
- WhatsApp distributor
- Jadwal kunjungan
- Status
- Action

Format jadwal:

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

- Nama distributor
- Nama sales
- No WA sales
- No WA distributor
- Interval kunjungan
- Hari kunjungan
- Foto
- Keterangan
- Status

Validasi nomor WhatsApp secara wajar tanpa terlalu ketat.

---

# 18. Halaman Pesanan

## List

Tampilkan:

- ID pesanan
- Distributor
- Tanggal
- Jumlah item
- Total
- Status
- Action

## Buat Pesanan

Flow:

1. Pilih distributor
2. Pilih barang
3. Masukkan jumlah
4. Harga beli otomatis diambil dari relasi BarangDistributor jika tersedia
5. Hitung subtotal
6. Bisa menambahkan beberapa barang
7. Hitung total
8. Simpan pesanan

Jangan membuat satu pesanan hanya untuk satu barang.

Satu pesanan harus dapat memiliki banyak barang.

---

# 19. Halaman Retur

## List

Tampilkan:

- ID retur
- Barang
- Distributor
- Jumlah
- Alasan
- Tanggal
- Status
- Action

## Form

Field:

- Barang
- Distributor
- Jumlah retur
- Alasan retur
- Foto
- Keterangan
- Tanggal retur
- Status

---

# 20. Upload Foto

Untuk versi pertama:

- Simpan file pada filesystem lokal.
- Gunakan folder yang jelas, misalnya:

```text
public/uploads/
├── barang/
├── distributor/
└── retur/
```

Nama file harus dibuat unik.

Jangan menggunakan nama file asli sebagai nama file final jika berpotensi collision.

Validasi:

- MIME type
- extension
- ukuran file
- hanya image yang diizinkan

Buat batas ukuran file yang wajar.

Jika foto tidak tersedia, tampilkan placeholder.

Jangan menyimpan binary image langsung di SQLite.

---

# 21. API / Server Logic

Pisahkan business logic dari UI sebanyak mungkin.

Jangan menaruh query Prisma besar langsung di banyak component.

Gunakan helper/service/repository jika diperlukan.

Semua operasi database harus:

- tervalidasi
- menangani error
- menggunakan Prisma
- tidak membocorkan error internal kepada user

Response API harus konsisten.

Contoh:

```json
{
  "success": true,
  "data": {}
}
```

Error:

```json
{
  "success": false,
  "message": "Data barang tidak ditemukan"
}
```

---

# 22. Validasi

Gunakan validation library yang ringan, misalnya **Zod**.

Validasi dilakukan di server.

Client-side validation hanya sebagai UX tambahan.

Jangan mengandalkan validasi client saja.

Validasi minimal:

### Barang

- nama wajib
- harga valid
- barcode unique jika diisi

### Distributor

- nama distributor wajib
- interval hanya 1 atau 2
- hari kunjungan harus valid

### Pesanan

- distributor wajib
- minimal satu detail
- jumlah > 0
- barang harus valid

### Retur

- barang wajib
- distributor wajib
- jumlah > 0
- status valid

---

# 23. Database Integrity

Gunakan foreign key relation Prisma.

Gunakan constraint yang sesuai.

Contoh:

- barcode unique
- barang + distributor unique
- detail pesanan tidak boleh memiliki jumlah <= 0

Hindari cascade delete yang dapat menghapus histori penting secara tidak sengaja.

Jika data sudah memiliki histori pesanan/retur, lebih aman menggunakan `status = NONAKTIF` daripada menghapus data master secara permanen.

---

# 24. Delete Strategy

Untuk master data:

### Barang

Lebih baik:

```text
status = AKTIF
status = NONAKTIF
```

daripada hard delete jika sudah digunakan pada transaksi/pesanan/retur.

### Distributor

Gunakan pendekatan yang sama.

### Pesanan

Hard delete hanya jika masih `DRAFT`.

Pesanan yang sudah diproses sebaiknya tidak sembarangan dihapus.

### Retur

Jangan hard delete histori retur tanpa alasan.

---

# 25. Search

Implementasikan search pada:

### Barang

- nama
- barcode

### Distributor

- nama distributor
- nama sales
- nomor WhatsApp

### Pesanan

- ID
- distributor

### Retur

- ID
- barang
- distributor

Gunakan debounce pada search jika search dilakukan secara realtime.

---

# 26. Format Harga

Gunakan Rupiah.

Contoh:

```text
Rp 12.500
Rp 1.250.000
```

Database tetap menyimpan angka, bukan string yang sudah diformat.

Jangan menyimpan:

```text
"Rp 12.500"
```

Simpan:

```text
12500
```

---

# 27. Format Tanggal

Database gunakan tipe DateTime.

UI Indonesia:

```text
16 Agustus 2026
```

Untuk timestamp:

```text
16 Agu 2026, 14:30
```

Perhatikan timezone Indonesia/WIB pada tampilan.

---

# 28. Dashboard

Dashboard tidak perlu terlalu kompleks.

Card:

```text
Total Barang
Total Distributor
Total Pesanan
Total Retur
```

Kemudian:

### Pesanan terbaru

Tampilkan 5-10 data terbaru.

### Retur terbaru

Tampilkan 5-10 data terbaru.

### Jadwal distributor

Tampilkan distributor berdasarkan hari kunjungan.

---

# 29. Performance

Prioritaskan aplikasi ringan.

Hindari:

- library besar yang tidak diperlukan
- animasi berlebihan
- request API berulang
- query database yang tidak diperlukan
- loading seluruh database sekaligus jika datanya besar

Gunakan:

- pagination
- select field Prisma seperlunya
- server-side fetching untuk data yang cocok
- loading state
- skeleton jika diperlukan

---

# 30. Error Handling

Setiap operasi CRUD harus memiliki:

- loading state
- success feedback
- error feedback
- empty state
- confirmation sebelum operasi berisiko

Contoh:

```text
Barang berhasil ditambahkan
Distributor berhasil diperbarui
Pesanan berhasil dibuat
Retur berhasil disimpan
```

Jika error:

```text
Gagal menyimpan data. Silakan coba lagi.
```

Jangan tampilkan stack trace/database error mentah kepada user.

---

# 31. Empty State

Jika belum ada data:

```text
Belum ada barang.

[ + Tambah Barang ]
```

Buat empty state yang jelas dan tidak hanya menampilkan table kosong.

---

# 32. Confirmation

Untuk aksi destruktif:

```text
Apakah Anda yakin ingin menonaktifkan barang ini?
```

Untuk data histori, prefer nonaktif daripada hapus permanen.

---

# 33. Seed Data

Buat Prisma seed sederhana untuk development.

Isi contoh:

- beberapa barang
- beberapa distributor
- relasi barang-distributor
- beberapa pesanan
- detail pesanan
- beberapa retur

Jangan gunakan data sensitif/nyata.

---

# 34. Environment

Gunakan `.env`.

Minimal:

```env
DATABASE_URL="file:./dev.db"
```

Jangan hardcode credential atau konfigurasi sensitif.

Buat `.env.example`.

---

# 35. Prisma

Buat:

```text
prisma/
├── schema.prisma
└── seed.ts
```

Pastikan migration dapat dijalankan dengan jelas.

Dokumentasikan command utama di README:

```bash
npm install
npx prisma generate
npx prisma migrate dev
npm run dev
```

Sesuaikan command jika package manager project berbeda.

---

# 36. Development Workflow

Sebelum coding:

1. Inspect project existing.
2. Jangan overwrite file existing secara membabi buta.
3. Identifikasi package manager.
4. Identifikasi versi Next.js.
5. Identifikasi apakah Prisma sudah ada.
6. Identifikasi apakah database sudah ada.
7. Pertahankan fitur existing yang masih relevan.

Kemudian:

1. Setup database
2. Buat Prisma schema
3. Migration
4. Seed
5. Setup layout
6. Setup components
7. Buat CRUD Barang
8. Buat CRUD Distributor
9. Buat Pesanan + DetailPesanan
10. Buat Retur
11. Buat Dashboard
12. Validasi
13. Testing
14. Perbaiki error
15. Final cleanup

---

# 37. Coding Rules

Gunakan TypeScript secara konsisten.

Hindari:

```typescript
any
```

kecuali benar-benar diperlukan.

Gunakan reusable components.

Jangan membuat component yang sama berulang-ulang jika dapat dibuat reusable.

Gunakan naming yang konsisten.

Contoh:

```text
BarangTable
BarangForm
DistributorTable
DistributorForm
PesananForm
PesananDetail
ReturForm
```

---

# 38. Prinsip Maintenance

Project harus mudah dipahami developer lain.

Prioritaskan:

- kode sederhana
- struktur jelas
- naming jelas
- fungsi kecil
- validasi terpusat
- database relation jelas
- komentar hanya jika diperlukan
- jangan over-engineering

Jangan membuat abstraction berlebihan untuk project sederhana.

---

# 39. Security Basic

Walaupun belum ada login:

- validasi input server-side
- validasi upload file
- batasi file upload
- sanitasi input jika diperlukan
- jangan expose path filesystem internal
- jangan expose stack trace
- gunakan Prisma query parameterization
- jangan menggunakan raw SQL kecuali benar-benar diperlukan

---

# 40. Acceptance Criteria

Project dianggap selesai apabila:

- aplikasi dapat dijalankan secara lokal
- database SQLite berhasil dibuat
- Prisma migration berhasil
- seed berhasil
- CRUD Barang berfungsi
- CRUD Distributor berfungsi
- relasi BarangDistributor berfungsi
- Pesanan dapat memiliki banyak barang
- Detail pesanan dapat dihitung
- Retur dapat dibuat
- Dashboard menampilkan data aktual
- upload foto berfungsi
- search berfungsi
- filter berfungsi
- validation berfungsi
- responsive di desktop dan mobile
- tidak ada error TypeScript
- tidak ada error build
- tidak ada query database yang jelas-jelas redundant
- UI konsisten
- README tersedia

---

# 41. Perintah Verifikasi

Sebelum menyatakan selesai, jalankan:

```bash
npm run lint
npm run build
```

Jika project memiliki test:

```bash
npm test
```

Perbaiki semua error yang muncul.

Jangan mengatakan project selesai jika build masih gagal.

---

# 42. Prioritas Implementasi

Gunakan urutan prioritas:

### P0 — Core

- Database
- Prisma
- Barang
- Distributor
- BarangDistributor

### P1 — Operational

- Pesanan
- DetailPesanan
- Retur

### P2 — UX

- Dashboard
- Search
- Filter
- Pagination
- Upload foto
- Toast
- Loading state
- Empty state

### P3 — Polish

- Responsive
- UI refinement
- Performance
- Error handling
- Documentation

---

# 43. Instruksi Utama Untuk AI Agent

Kerjakan project ini secara langsung berdasarkan spesifikasi di atas.

Jangan hanya memberikan contoh kode atau menjelaskan langkah-langkah.

Jika project sudah memiliki kode:

1. Inspect terlebih dahulu.
2. Pertahankan bagian yang masih relevan.
3. Modifikasi hanya bagian yang diperlukan.
4. Jangan merusak fitur existing.

Jika ada keputusan teknis kecil yang tidak disebutkan:

- pilih solusi paling sederhana
- pilih solusi yang mudah di-maintain
- prioritaskan compatibility dengan Next.js + Prisma + SQLite
- jangan menambahkan dependency tanpa alasan jelas

Jangan menambahkan fitur di luar scope.

Jika menemukan konflik antara implementasi existing dan spesifikasi ini, prioritaskan keamanan data dan stabilitas aplikasi, lalu pilih solusi yang paling minim perubahan.

Setelah implementasi:

1. Jalankan lint.
2. Jalankan build.
3. Perbaiki error.
4. Pastikan migration database valid.
5. Pastikan CRUD utama dapat digunakan.
6. Pastikan UI responsive.
7. Pastikan tidak ada placeholder penting yang tertinggal.

Tujuan akhirnya adalah menghasilkan aplikasi **Manajemen Toko yang benar-benar runnable**, bukan sekadar prototype atau kumpulan contoh kode.
