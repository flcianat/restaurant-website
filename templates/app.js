var bukuUrl = "{{ url_for('buku') }}";
var anggotaUrl = "{{ url_for('data_anggota') }}";
var peminjamanUrl = "{{ url_for('peminjaman') }}";
var dendaUrl = "{{ url_for('denda') }}";

function showDashboard() {
  document.getElementById("dashboard").style.display = "block";
  document.getElementById("content").style.display = "none";
  history.replaceState(null, null, window.location.pathname);
}

function loadContent(url) {
  fetch(url)
    .then((response) => response.text())
    .then((data) => {
      document.getElementById("content").innerHTML = data;
      document.getElementById("dashboard").style.display = "none";
      document.getElementById("content").style.display = "block";
      window.location.hash = url;
    });
}

window.onload = function () {
  // Cek apakah hash URL sudah ada
  if (window.location.hash) {
    // Jika ada, muat konten sesuai dengan hash URL
    loadContent(window.location.hash.slice(1)); // Potong tanda '#' dari hash URL
  } else {
    // Jika tidak ada hash, tampilkan dashboard
    showDashboard();
  }
};
