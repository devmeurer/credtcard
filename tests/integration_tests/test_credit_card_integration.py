class TestCreditCardIntegration:
    def test_full_user_flow(self, client, token, db_session):
        card_data = {
            "exp_date": "2024-07-01",
            "holder": "John Doe",
            "number": "4539578763621486",
            "cvv": "123",
        }
        headers = {"Authorization": f"Bearer {token}"}

        # Test create operation
        response = client.post("api/v1/credit-card", headers=headers, json=card_data)
        assert response.status_code == 200
        created_card = response.json()

        # Test read operation
        response = client.get(
            f"api/v1/credit-card/{created_card['id']}", headers=headers
        )
        assert response.status_code == 200
        assert response.json() == created_card

        # Test update operation
        update_data = {
            "exp_date": created_card["exp_date"],
            "holder": "Jane Doe",
            "number": created_card["number"],
            "cvv": created_card["cvv"],
            "brand": created_card["brand"],
        }

        response = client.put(
            f"api/v1/credit-card/{created_card['id']}",
            headers=headers,
            json=update_data,
        )
        assert response.status_code == 200
        created_card.update(update_data)
        assert response.json() == created_card

        # Test delete operation
        response = client.delete(
            f"api/v1/credit-card/{created_card['id']}", headers=headers
        )
        assert response.status_code == 200
        assert response.json() == {"message": "Credit card deleted successfully"}

        # Confirm deletion
        response = client.get(
            f"api/v1/credit-card/{created_card['id']}", headers=headers
        )
        assert response.status_code == 404
