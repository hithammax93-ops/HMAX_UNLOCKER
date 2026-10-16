import unittest

from main import app
import hmax_dump_tools


class WebRouteTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home_displays_neon_page(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"HMAX UNLOCKER", response.data)

    def test_light_route_displays_neon_page(self):
        response = self.client.get("/light")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"HMAX UNLOCKER", response.data)

    def test_health_returns_exact_ok_json(self):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "ok"})


class DumpToolsApiTests(unittest.TestCase):
    """The DUMP source tools must be reachable outside Telegram too."""

    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()

    def test_dump_tools_lists_every_tool_with_its_download_link(self):
        payload = self.client.get("/api/dump-tools").get_json()

        self.assertEqual(payload["count"], len(hmax_dump_tools.DUMP_TOOLS))
        self.assertEqual(payload["total_cards"], sum(
            len(cards) for cards in hmax_dump_tools.DUMP_CARDS.values()
        ))
        for tool in payload["tools"]:
            with self.subTest(tool=tool["id"]):
                self.assertTrue(tool["download_url"], "tool has no download link")
                self.assertEqual(tool["cards_count"], len(tool["cards"]))
                self.assertTrue(tool["name"])

    def test_dump_tools_filters_by_category(self):
        jtag = self.client.get("/api/dump-tools?category=jtag").get_json()
        normal = self.client.get("/api/dump-tools?category=normal").get_json()

        self.assertEqual(
            {t["id"] for t in jtag["tools"]},
            {"easy_jtag", "f64_ultra", "ufi"},
        )
        self.assertEqual(
            {t["id"] for t in normal["tools"]},
            {"unlocktool", "cm2", "pandora", "amt", "miracle"},
        )
        self.assertEqual(jtag["count"] + normal["count"], len(hmax_dump_tools.DUMP_TOOLS))

    def test_dump_tools_single_tool_lookup(self):
        payload = self.client.get("/api/dump-tools?tool=pandora&lang=en").get_json()

        self.assertEqual(payload["count"], 1)
        tool = payload["tools"][0]
        self.assertEqual(tool["name"], "Pandora Tool")
        self.assertEqual(tool["download_label"], "⬇️ Download Pandora Tool")

    def test_dump_tools_rejects_unknown_category(self):
        response = self.client.get("/api/dump-tools?category=bogus")

        self.assertEqual(response.status_code, 400)

    def test_dump_tools_404s_on_unknown_tool(self):
        response = self.client.get("/api/dump-tools?tool=does_not_exist")

        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
