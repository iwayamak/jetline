# -*- coding: utf-8 -*-


class Config(object):
    AVAILABLE_SUB_MODULE = (
        'PostgreSQLProcessing',
        'PostgreSQLCopy',
        'LocalProcessing',
        'S3',
        'Confluence',
        'Scp',
        'Plugin'
    )

    CONVERT_CHARSET_LIST = (
        'utf_8',
        'utf_8_sig',
        'shift_jis',
        'shift_jis_2004',
        'shift_jisx0213',
        'euc_jp',
        'euc_jis_2004',
        'euc_jisx0213',
        'cp932',
        'iso2022_jp',
        'iso2022_jp_1',
        'iso2022_jp_2',
        'iso2022_jp_2004',
        'iso2022_jp_3',
        'iso2022_jp_ext',
        'utf_32',
        'utf_32_be',
        'utf_32_le',
        'utf_16',
        'utf_16_be',
        'utf_16_le',
        'utf_7'
    )
