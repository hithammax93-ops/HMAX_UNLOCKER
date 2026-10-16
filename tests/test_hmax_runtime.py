import os
import tempfile
import unittest

from hmax_runtime import BannedUserCache, TTLCache, iter_document_pages


class FakeDocument:
    def __init__(self, document_id):
        self.id = document_id


class FakeQuery:
    def __init__(self, documents, page_size=None, cursor=None):
        self.documents = documents
        self.page_size = page_size
        self.cursor = cursor

    def limit(self, page_size):
        return FakeQuery(self.documents, page_size, self.cursor)

    def start_after(self, cursor):
        return FakeQuery(self.documents, self.page_size, cursor.id)

    def stream(self):
        documents = self.documents
        if self.cursor is not None:
            cursor_index = next(
                index for index, doc in enumerate(documents)
                if doc.id == self.cursor
            )
            documents = documents[cursor_index + 1:]
        return iter(documents[:self.page_size])


class FakeCollection:
    def __init__(self, document_ids):
        self.documents = [FakeDocument(doc_id) for doc_id in document_ids]

    def order_by(self, field_path):
        if field_path != "__name__":
            raise AssertionError("expected document-ID ordering")
        return FakeQuery(self.documents)


class RuntimeHelperTests(unittest.TestCase):
    def test_ban_ids_are_cached_and_updated_atomically(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = os.path.join(temp_dir, "banned_users.txt")
            cache = BannedUserCache(path)

            self.assertEqual(cache.ids(), set())
            cache.update_local("42", True)
            self.assertEqual(cache.ids(), {"42"})
            self.assertIs(cache.get_status("42"), True)

            restarted_cache = BannedUserCache(path)
            self.assertEqual(restarted_cache.ids(), {"42"})

            cache.update_local("42", False)
            self.assertEqual(cache.ids(), set())
            self.assertIsNone(cache.get_status("42"))

    def test_status_cache_can_be_invalidated(self):
        cache = BannedUserCache("unused.txt")
        cache.set_status("7", False)
        self.assertIs(cache.get_status("7"), False)
        cache.invalidate_status("7")
        self.assertIsNone(cache.get_status("7"))

    def test_status_cache_expires_immediately_when_ttl_is_zero(self):
        cache = TTLCache(ttl_seconds=0)
        cache.set("member", True)
        self.assertIsNone(cache.get("member"))

    def test_status_cache_evicts_oldest_when_full(self):
        cache = TTLCache(ttl_seconds=60, max_entries=2)
        cache.set("first", True)
        cache.set("second", False)
        cache.set("third", True)
        self.assertIsNone(cache.get("first"))
        self.assertIs(cache.get("third"), True)

    def test_firestore_documents_are_yielded_in_bounded_pages(self):
        collection = FakeCollection(["a", "b", "c", "d", "e"])
        pages = list(iter_document_pages(collection, page_size=2))
        self.assertEqual(
            [[doc.id for doc in page] for page in pages],
            [["a", "b"], ["c", "d"], ["e"]],
        )

    def test_firestore_page_size_must_be_positive(self):
        with self.assertRaises(ValueError):
            list(iter_document_pages(FakeCollection([]), page_size=0))


if __name__ == "__main__":
    unittest.main()
