from http import client

from main.tests import BasicTest

# Create your tests here.


class BookHolderTests(BasicTest):
    def setUp(self):
        (token) = self.get_or_create_librarian_token()
        self.headers = {'HTTP_AUTHORIZATION': f'Token {token}'}
        self.url = f'{self.base_url}'
        return super().setUp()

    def test_create(self):
        request_payload = {
            'name': 'user1'
        }
        response = self.client.post(
            self.url,
            request_payload,
            **self.headers
        )
        self.assertEqual(response.status_code, 201)

    def test_list(self):
        response = self.client.get(
            self.url, **self.headers)
        self.assertEqual(response.status_code, 200)

    def test_update(self):
        holder = self.get_or_create_bookholder()
        request_payload = {
            'name': 'name'
        }
        response = self.client.put(
            f'{self.url}{holder.id}/', request_payload, **self.headers
        )
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        holder = self.get_or_create_bookholder()
        response = self.client.delete(
            f'{self.url}{holder.id}/', **self.headers
        )
        self.assertEqual(response.status_code, 204)
