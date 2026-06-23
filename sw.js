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

// 文字起こし・要約のAPIは常に最新を取りに行き、画面部品はオフラインでも出す
self.addEventListener('fetch', (e) => {
  const url = new URL(e.request.url);
  if (url.pathname.startsWith('/transcribe') || url.pathname.startsWith('/summarize')) {
    return; // APIはネット必須なのでキャッシュしない
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
