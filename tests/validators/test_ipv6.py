from util import case


@case({
    'ipv6': {
        'valid': [
            '2001:0DB8:02de:0000:0000:0000:0000:0e13',
            '2001:DB8:2de:0000:0000:0000:0000:e13',
            '2001:DB8:2de:000:000:000:000:e13',
            '2001:DB8:2de:00:00:00:00:e13',
            '2001:DB8:2de:0:0:0:0:e13',
            '2001:DB8:2de::e13',
            '2001:0DB8:0000:0000:0000:0000:1428:57ab',
            '2001:0DB8:0000:0000:0000::1428:57ab',
            '2001:0DB8:0:0:0:0:1428:57ab',
            '2001:0DB8:0::0:1428:57ab',
            '2001:0DB8::1428:57ab',
            '0000:0000:0000:0000:0000:ffff:874B:2B34',
            '::ffff:135.75.43.52',
            '::1',
        ],
        'invalid': [
            '2001::25de::cade',
            '127.0.0.1'
        ]
    }
})
def test_ipv6():
    pass
