// 高坂先生のメモAI – サービスワーカー（スマホアプリ化用）
const CACHE = 'kosaka-memo-v1';
const SHELL = ['/', 'index.html', 'manifest.json', 'robot.png', 'icon.png'];

// インストール時：画面の部品をキャッシュ
self.addEventListener('install', (e) => {
  self.skipWaiting();
  e.waitUntil(
    caches.open(CACHE).then((c) => c.addAll(SHELL).catch(() => {}))
  );
});

// 古いキャッシュを掃除
self.addEventListener('activate', (e) => {
  self.clients.claim();
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    )
  );
});

// Groqへの通信は常にネットへ。画面部品（同一オリジン）だけオフライン対応する
self.addEventListener('fetch', (e) => {
  // 別オリジン（Groq APIなど）はキャッシュに触れず、そのまま通す
  if (new URL(e.request.url).origin !== self.location.origin) {
    return;
  }
  e.respondWith(
    fetch(e.request)
      .then((res) => {
        const copy = res.clone();
        caches.open(CACHE).then((c) => c.put(e.request, copy)).catch(() => {});
        return res;
      })
      .catch(() => caches.match(e.request))
  );
});
