import lib
import unittest

"""
テスト用の値は全て以下のページからの引用である

https://developer.twitter.com/en/docs/basics/authentication/guides/authorizing-a-request
https://developer.twitter.com/en/docs/basics/authentication/guides/creating-a-signature
"""


class OAuthTest(unittest.TestCase):
    token_secret = "LswwdoUaIvS8ltyTt5jkRh4J50vUPVVHtR2YPi5kE"
    consumer_secret = "kAcSOqF21Fu85e7zjz7ZN2U4ZRhfV3WpwPAoE3Z7kBw"
    nonce = "kYjzVBB8Y0ZFabxSWbWovY3uYSQ2pTgmZeNu2VS4cg"
    timestamp = "1318622958"
    token = "370773112-GmHxMAgYyLbNEtIKZeRNFsMKPR9EyMZeS9weJAEb"
    consumer = "xvz1evFS4wEEPTGEFPHBog"
    param = [("status", "Hello Ladies + Gentlemen, a signed OAuth request!"),
             ("include_entities", "true")
             ]
    url = "https://api.twitter.com/1/statuses/update.json"
    signature = "tnnArxj06cWHq44gCs1OSKk/jLY="

    def test_key(self):
        self.assertEqual("kAcSOqF21Fu85e7zjz7ZN2U4ZRhfV3WpwPAoE3Z7kBw&LswwdoUaIvS8ltyTt5jkRh4J50vUPVVHtR2YPi5kE",
                         lib.create_hmac_key(self.consumer_secret, self.token_secret))

    def test_signature(self):
        key = lib.create_hmac_key(self.consumer_secret, self.token_secret)
        auth_base = lib.create_auth_base(self.consumer, self.token, self.nonce, self.timestamp)
        signature = lib.create_signature(True, self.url, self.param, auth_base, key)
        self.assertEqual(self.signature, signature)

    def test_create_auth_header(self):
        auth_base = lib.create_auth_base(self.consumer, self.token, self.nonce, self.timestamp)
        header = 'OAuth oauth_consumer_key="xvz1evFS4wEEPTGEFPHBog", ' \
                 'oauth_nonce="kYjzVBB8Y0ZFabxSWbWovY3uYSQ2pTgmZeNu2VS4cg", ' \
                 'oauth_signature="tnnArxj06cWHq44gCs1OSKk%2FjLY%3D", ' \
                 'oauth_signature_method="HMAC-SHA1", oauth_timestamp="1318622958", ' \
                 'oauth_token="370773112-GmHxMAgYyLbNEtIKZeRNFsMKPR9EyMZeS9weJAEb", ' \
                 'oauth_version="1.0"'
        self.assertEqual(header, lib.create_auth_header(auth_base, self.signature))


if __name__ == "__main__":
    unittest.main()
