"""Small, testable runtime helpers used by the HMAX Telegram bot."""

import os
import threading
import time


class BannedUserCache:
    """Cache local ban IDs and short-lived Firebase ban lookups."""

    def __init__(self, path, status_ttl_seconds=30):
        self.path = path
        self.status_ttl_seconds = max(0, float(status_ttl_seconds))
        self._lock = threading.RLock()
        self._local_ids = None
        self._status = {}

    def ids(self):
        with self._lock:
            if self._local_ids is None:
                try:
                    with open(self.path, "r", encoding="utf-8") as banned_file:
                        self._local_ids = {
                            line.strip()
                            for line in banned_file
                            if line.strip()
                        }
                except FileNotFoundError:
                    self._local_ids = set()
            return set(self._local_ids)

    def update_local(self, user_id, banned):
        uid = str(user_id)
        with self._lock:
            ids = self.ids()
            if banned:
                ids.add(uid)
            else:
                ids.discard(uid)

            temporary_path = self.path + ".tmp"
            with open(temporary_path, "w", encoding="utf-8") as banned_file:
                banned_file.write("\n".join(sorted(ids)))
            os.replace(temporary_path, self.path)
            self._local_ids = ids

            # Always drop any cached verdict first so a stale result (in either
            # direction) cannot linger after a ban/unban transition. When the
            # user is unbanned we intentionally leave the entry empty so the
            # next lookup re-reads the durable state from Firebase.
            self._status.pop(uid, None)
            if banned:
                self._status[uid] = (
                    True,
                    time.monotonic() + self.status_ttl_seconds,
                )

    def get_status(self, user_id):
        uid = str(user_id)
        now = time.monotonic()
        with self._lock:
            entry = self._status.get(uid)
            if entry is None:
                return None
            banned, expires_at = entry
            if expires_at <= now:
                self._status.pop(uid, None)
                return None
            return banned

    def set_status(self, user_id, banned):
        uid = str(user_id)
        with self._lock:
            self._status[uid] = (
                bool(banned),
                time.monotonic() + self.status_ttl_seconds,
            )

    def invalidate_status(self, user_id):
        with self._lock:
            self._status.pop(str(user_id), None)


def iter_document_pages(collection_ref, page_size=200):
    """Yield bounded Firestore document pages using a document-ID cursor."""
    page_size = int(page_size)
    if page_size < 1:
        raise ValueError("page_size must be at least 1")

    ordered_query = collection_ref.order_by("__name__")
    cursor = None
    while True:
        page_query = ordered_query.limit(page_size)
        if cursor is not None:
            page_query = page_query.start_after(cursor)
        page = list(page_query.stream())
        if not page:
            return
        yield page
        cursor = page[-1]
        if len(page) < page_size:
            return

class TTLCache:
    """Thread-safe, bounded cache for short-lived boolean status checks."""

    def __init__(self, ttl_seconds=15, max_entries=10000):
        self.ttl_seconds = max(0, float(ttl_seconds))
        self.max_entries = max(1, int(max_entries))
        self._lock = threading.RLock()
        self._values = {}

    def get(self, key):
        now = time.monotonic()
        with self._lock:
            entry = self._values.get(key)
            if entry is None:
                return None
            value, expires_at = entry
            if expires_at <= now:
                self._values.pop(key, None)
                return None
            return value

    def set(self, key, value):
        now = time.monotonic()
        with self._lock:
            expired = [
                cache_key
                for cache_key, (_, expires_at) in self._values.items()
                if expires_at <= now
            ]
            for cache_key in expired:
                self._values.pop(cache_key, None)
            if len(self._values) >= self.max_entries and key not in self._values:
                oldest_key = min(
                    self._values,
                    key=lambda cache_key: self._values[cache_key][1],
                )
                self._values.pop(oldest_key, None)
            self._values[key] = (value, now + self.ttl_seconds)

    def invalidate(self, key):
        with self._lock:
            self._values.pop(key, None)
