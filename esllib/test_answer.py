from unittest import TestCase

from esllib.Package import Answer


class TestAnswer(TestCase):
	def test_answer_susccess(self):
		self.assertEqual("@00124E23061C95AD541F11", Answer(service_code=20003, display_tag_id="061C95", rssi=-81, tag_status=84, volt=3.1, temperature=17).__repr__())
		self.assertEqual("@001299D1061C95DB541F19", Answer(service_code=39377, display_tag_id="061C95", rssi=-35, tag_status=84, volt=3.1, temperature=25).__repr__())

	def test_answer_raw_decode(self):
		self.assertEqual("@00124E23061C95AD541F11", Answer("@00124E23061C95AD541F11").__repr__())
		self.assertEqual("@001299D1061C95DB541F19", Answer("@001299D1061C95DB541F19").__repr__())
