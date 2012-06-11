from django.test import TestCase


class EntryTests(TestCase):
    def test_entry_archive_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mingus/entry_index.html')
