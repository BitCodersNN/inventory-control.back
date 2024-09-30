# flake8: noqa

from typing import Final

PUBLIC_KEY_RSA: Final = {
    'alg': 'RS256',
    'kty': 'RSA',
    'n': 'qAq_-0IuKCo3jm6R0jKKwjVD2V2vLCS0Kjj4kQHRdAPeG-i17y5_wYBNfGJI1gxRfDFj8QWB64XnjRfIrSYxHelRL'
         '-FULrZHU0e4i2D2OyvblN_6adx8MixYUI92Libm49r9eb9QH22_u0FWjQRtqNP4m2gxZ70wQp6z2Lh47A3pM21'
         '-F8G7ORxDcydi2oOYCCMoy3BJRrBULIUGx8STowWgcl1IQRYsDLUsFPFlsmj1JreoExMTCN9ivvfLZnqrZnrWE6tV'
         '-VotNW2lBbVXfF1qHVBj5jsgAWfX0BkgGHnzzPLtI61qlHSjW5onz6F7HNUvYVvMntbU0LBX25PvaQ',
    'e': 'AQAB',
}

WRONG_PUBLIC_KEY_RSA: dict = {
    'alg': 'RS256',
    'kty': 'RSA',
    'n': 'qAq_-0IuKCo3jm6R0jKKwjVD2V2vLCS0Kjj4kQHRdAPeG-i17y5_wYBNfGJI1gxRfDFj8QWB64XnjRfIrSYxHelRL'
         '-FULrZHU0e4i2D2OyvblN_6adx8MfdYUI92Libm49r9eb9QH22_u0FWjQRtqNP4m2gxZ70wQp6z2Lh47A3pM21'
         '-F8G7ORxDcydi2oOYCCMoy3BJRrBULIUGx8STowWgcl1IQRYsDLUsFPFlsmj1JreoExMTCN9ivvfLZnqrZnrWE6tV'
         '-VotNW2lBbVXfF1qHVBj5jsgAWfx0BcgGHnzzPLtI61qlHSjW5onz6F7HNUvYVvMntbU0LBX25PvaQ',
    'e': 'AQAB',
}

SECRET_KEY_RSA: dict = {
    'alg': 'RS256',
    'kty': 'RSA',
    'n': 'qAq_-0IuKCo3jm6R0jKKwjVD2V2vLCS0Kjj4kQHRdAPeG-i17y5_wYBNfGJI1gxRfDFj8QWB64XnjRfIrSYxHelRL'
         '-FULrZHU0e4i2D2OyvblN_6adx8MixYUI92Libm49r9eb9QH22_u0FWjQRtqNP4m2gxZ70wQp6z2Lh47A3pM21'
         '-F8G7ORxDcydi2oOYCCMoy3BJRrBULIUGx8STowWgcl1IQRYsDLUsFPFlsmj1JreoExMTCN9ivvfLZnqrZnrWE6tV'
         '-VotNW2lBbVXfF1qHVBj5jsgAWfX0BkgGHnzzPLtI61qlHSjW5onz6F7HNUvYVvMntbU0LBX25PvaQ',
    'e': 'AQAB',
    'd': 'IoOGt9_5Y_V70KzEFYSc_FN9WoVD59CoEm3-G6ZgczAiK-BJkdUel0s3Xv8'
         '-z3vbNqNcUBIeA5ZOnyuN44ZPG0IjEy74H9n_X0sBS9s_55pT8MlqANkwxwtVnkJA9yy1SoJdgmZ5WeMsOJUsZi1NKppS2vR1BUYVxfEbpj0JVQ4XJHgkh4rs4gsdBw-OEp3wYYruKEM4fppuDHGxol9Zfpd5wfUW0LFqvmAz_nJ-FZ32nyIxyaTipzLx2_i9ZQO9GLLEeEMbbHidzWTPnBoQeotQgPGov8vZtO9dM10qGL0r-YoNTVqma0MBHwROcjsbpkx-917-eWfkz_jKmEO3aQ',
    'p': '1ezFbwxPbhvNYtaaYUK26IIrBwjaj65bjoxnm56yBPcY_oIlJMve9n7n5cesJcTbPCnl5jZ6yWwlaHNwxPJ_QFaROQ64Fmvmu5'
         '-rFZsoQIbOD6O-zBmoGkHhMQ3HuPR5RkYuXgiIykdNrf8o0rf7o4sIYoSkxpqAxTu7oEd7YfU',
    'q': 'yRfATEpmIXelhlr7ijNLpPfk8qNIVVd_hd4yUYz1YqKWNwHrRQU17Th3Y5jepzm2dLfrHr39moGapLjuG85dkjaSCfn0umlJSxJ2fsbOneTpwemEx77yEWHR58xhotKnqqts-MjjdCa-3MAonY11Iz8Q96gU6WyjAYoHG1lcSyU',
    'dp': 'hwePy7tye6by6ltZUOECgRqAvEz7YEwHIKBBWbo-1eF-lk9h0Ksazm5mQ-TYJXLvizdLFRf4QyGPLzIG0Vnbtqmtut0ul4B'
          '-QJnVLKsmKiys7rRF36CmOgSxdvwiv_0Ye6Ia7GHorf1568UuaGuXW7CLl1vwgifN9jDxCod0Ou0',
    'dq': 'fGnwdIL3Sy9-PnDd_bQc0fT5NlFleD'
          '-JS2aclS3zx9G1xFSwneRKZ_kujHVRE_817mK32i5L0CLtbYpo7tUvuT1__yIhko9_ZC4JGAiiXrf5FBsJJpfxpmVx'
          '-8rMgXN5frNO2WFYsE0keul8d3XEikkDk2XvgjfPZi1ilj4kRu0',
    'qi': 'HsTCEbXvGMNRcTU52uB3ImsXXGMefmTeHnDR9BMhl2Jo3nXrVcKxoYhAumVLgtowdr'
          '-AYdeuijkNHct119ynfgbGjAzJdPImuuADiCzxnSs6HW8KEd9pg1ZmMZG4L8dQBsut'
          'fjr2zH_gZIcA2KM6u4gcemo5pwhsIzATZniODgY',
}


SECRET_KEY_HS256: Final = 'secret'

ALGORITHM_HS256: Final = 'HS256'
ALGORITHM_RS256: Final = 'RS256'
