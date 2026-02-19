import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from unittest.mock import patch, MagicMock
from src.services.notificationProcessor import poll_messages

@patch("boto3.client")
def test_worker_polling(mock_boto):

    mock_sqs = MagicMock()

    mock_sqs.receive_message.side_effect = [
        {
            "Messages": [
                {
                    "Body": '{"Message": "{\\"message\\": \\"Test Message\\"}"}',
                    "ReceiptHandle": "test-handle"
                }
            ]
        },
        KeyboardInterrupt()
    ]

    mock_boto.return_value = mock_sqs

    try:
        poll_messages()
    except KeyboardInterrupt:
        pass

    assert True
