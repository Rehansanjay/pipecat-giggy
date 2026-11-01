"""TTS base URL validation stays offline and accepts only the public API path."""
from types import SimpleNamespace
import unittest

from pipecat_giggy.tts import GiggyHttpTTSService


class TTSBaseUrlTests(unittest.TestCase):
    def service(self, base_url: str = 'https://api.giggy.ai/v1') -> GiggyHttpTTSService:
        return GiggyHttpTTSService(
            api_key='unit-test-key',
            voice_id='00000000-0000-0000-0000-000000000000',
            aiohttp_session=SimpleNamespace(auth=None, headers={}),
            base_url=base_url,
        )

    def test_default_and_loopback_override(self) -> None:
        self.assertEqual(self.service()._speech_url, 'https://api.giggy.ai/v1/audio/speech')
        self.assertEqual(self.service('http://127.0.0.1:8080/v1')._speech_url, 'http://127.0.0.1:8080/v1/audio/speech')

    def test_rejects_unsafe_or_non_v1_urls(self) -> None:
        for url in (
            'http://api.giggy.ai/v1',
            'http://localhost.evil.example/v1',
            'https://user:password@api.giggy.ai/v1',
            'https://api.giggy.ai/private',
            'https://api.giggy.ai/v1?debug=1',
            'https://api.giggy.ai/v1?',
            'https://api.giggy.ai/v1#',
            'https://api.giggy.ai:/v1',
            'https://api.giggy.ai:99999/v1',
        ):
            with self.subTest(url=url), self.assertRaises(ValueError):
                self.service(url)
