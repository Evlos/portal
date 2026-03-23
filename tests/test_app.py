import json
import pytest


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def add_bookmark(client, url, title=""):
    return client.post("/add", data={"url": url, "title": title},
                       follow_redirects=True)

def get_ids(client):
    """从首页 HTML 中提取所有 data-id。"""
    html = client.get("/").data.decode()
    import re
    return [int(x) for x in re.findall(r'data-id="(\d+)"', html)]


# ─────────────────────────────────────────────
# 首页
# ─────────────────────────────────────────────

class TestIndex:
    def test_returns_200(self, client):
        res = client.get("/")
        assert res.status_code == 200

    def test_empty_state_shown(self, client):
        assert b"NO ENTRIES YET" in client.get("/").data

    def test_entry_appears_after_add(self, client):
        add_bookmark(client, "https://example.com", "Example")
        assert b"Example" in client.get("/").data
        assert b"https://example.com" in client.get("/").data


# ─────────────────────────────────────────────
# 新增
# ─────────────────────────────────────────────

class TestAdd:
    def test_add_with_title(self, client):
        res = add_bookmark(client, "https://python.org", "Python")
        assert res.status_code == 200
        assert b"Python" in res.data

    def test_add_without_title_uses_url(self, client):
        add_bookmark(client, "https://github.com")
        assert b"https://github.com" in client.get("/").data

    def test_add_without_url_redirects_safely(self, client):
        res = client.post("/add", data={"url": "", "title": "No URL"},
                          follow_redirects=True)
        assert res.status_code == 200
        assert b"NO ENTRIES YET" in res.data

    def test_sort_order_increments(self, client):
        add_bookmark(client, "https://a.com", "A")
        add_bookmark(client, "https://b.com", "B")
        add_bookmark(client, "https://c.com", "C")
        ids = get_ids(client)
        assert len(ids) == 3
        # 首页顺序应与插入顺序一致
        html = client.get("/").data.decode()
        assert html.index("https://a.com") < html.index("https://b.com") < html.index("https://c.com")


# ─────────────────────────────────────────────
# 删除
# ─────────────────────────────────────────────

class TestDelete:
    def test_delete_existing(self, client):
        add_bookmark(client, "https://delete-me.com", "DeleteMe")
        ids = get_ids(client)
        res = client.post(f"/delete/{ids[0]}")
        assert res.status_code == 200
        assert res.json["status"] == "ok"
        assert b"DeleteMe" not in client.get("/").data

    def test_delete_nonexistent_returns_ok(self, client):
        res = client.post("/delete/99999")
        assert res.status_code == 200
        assert res.json["status"] == "ok"


# ─────────────────────────────────────────────
# 编辑
# ─────────────────────────────────────────────

class TestEdit:
    def test_edit_title_and_url(self, client):
        add_bookmark(client, "https://old.com", "Old Title")
        item_id = get_ids(client)[0]

        res = client.post(f"/edit/{item_id}",
                          data=json.dumps({"title": "New Title", "url": "https://new.com"}),
                          content_type="application/json")
        assert res.status_code == 200
        data = res.json
        assert data["status"] == "ok"
        assert data["title"] == "New Title"
        assert data["url"]   == "https://new.com"

        html = client.get("/").data.decode()
        assert "New Title"       in html
        assert "https://new.com" in html
        assert "Old Title"       not in html

    def test_edit_empty_title_falls_back_to_url(self, client):
        add_bookmark(client, "https://foo.com", "Foo")
        item_id = get_ids(client)[0]
        res = client.post(f"/edit/{item_id}",
                          data=json.dumps({"title": "", "url": "https://foo.com"}),
                          content_type="application/json")
        assert res.json["title"] == "https://foo.com"

    def test_edit_missing_url_returns_400(self, client):
        add_bookmark(client, "https://foo.com", "Foo")
        item_id = get_ids(client)[0]
        res = client.post(f"/edit/{item_id}",
                          data=json.dumps({"title": "T", "url": ""}),
                          content_type="application/json")
        assert res.status_code == 400


# ─────────────────────────────────────────────
# 排序
# ─────────────────────────────────────────────

class TestReorder:
    def test_reorder_changes_display_order(self, client):
        add_bookmark(client, "https://first.com",  "First")
        add_bookmark(client, "https://second.com", "Second")
        add_bookmark(client, "https://third.com",  "Third")
        ids = get_ids(client)          # [1, 2, 3]
        reversed_ids = list(reversed(ids))  # [3, 2, 1]

        res = client.post("/reorder",
                          data=json.dumps(reversed_ids),
                          content_type="application/json")
        assert res.status_code == 200
        assert res.json["status"] == "ok"

        html = client.get("/").data.decode()
        assert html.index("https://third.com") < html.index("https://second.com") < html.index("https://first.com")

    def test_reorder_empty_list(self, client):
        res = client.post("/reorder",
                          data=json.dumps([]),
                          content_type="application/json")
        assert res.status_code == 200
        assert res.json["status"] == "ok"
