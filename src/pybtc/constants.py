# constants.py


MAX_AMOUNT = 2100000000000000
SIGHASH_ALL = 0x00000001
SIGHASH_NONE = 0x00000002
SIGHASH_SINGLE = 0x00000003
SIGHASH_ANYONECANPAY = 0x00000080
ECDSA_SEC256K1_ORDER = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141

MAINNET_ADDRESS_BYTE_PREFIX = b'\x00'
TESTNET_ADDRESS_BYTE_PREFIX = b'\x6f'
MAINNET_SCRIPT_ADDRESS_BYTE_PREFIX = b'\x05'
TESTNET_SCRIPT_ADDRESS_BYTE_PREFIX = b'\xc4'
MAINNET_SEGWIT_ADDRESS_BYTE_PREFIX = b'\x03\x03\x00\x02\x03'
TESTNET_SEGWIT_ADDRESS_BYTE_PREFIX = b'\x03\x03\x00\x14\x02'

MAINNET_ADDRESS_PREFIX = '1'
TESTNET_ADDRESS_PREFIX = 'm'
TESTNET_ADDRESS_PREFIX_2 = 'n'
MAINNET_SCRIPT_ADDRESS_PREFIX = '3'
TESTNET_SCRIPT_ADDRESS_PREFIX = '2'

MAINNET_PRIVATE_KEY_UNCOMPRESSED_PREFIX = '5'
MAINNET_PRIVATE_KEY_COMPRESSED_PREFIX = 'K'
MAINNET_PRIVATE_KEY_COMPRESSED_PREFIX_2 = 'L'
TESTNET_PRIVATE_KEY_UNCOMPRESSED_PREFIX = '9'
TESTNET_PRIVATE_KEY_COMPRESSED_PREFIX = 'c'

ADDRESS_PREFIX_LIST = (MAINNET_ADDRESS_PREFIX,
                       TESTNET_ADDRESS_PREFIX,
                       TESTNET_ADDRESS_PREFIX_2,
                       MAINNET_SCRIPT_ADDRESS_PREFIX,
                       TESTNET_SCRIPT_ADDRESS_PREFIX)

PRIVATE_KEY_PREFIX_LIST = (MAINNET_PRIVATE_KEY_UNCOMPRESSED_PREFIX,
                           MAINNET_PRIVATE_KEY_COMPRESSED_PREFIX,
                           MAINNET_PRIVATE_KEY_COMPRESSED_PREFIX_2,
                           TESTNET_PRIVATE_KEY_UNCOMPRESSED_PREFIX,
                           TESTNET_PRIVATE_KEY_COMPRESSED_PREFIX)

MAINNET_PRIVATE_KEY_BYTE_PREFIX = b'\x80'
TESTNET_PRIVATE_KEY_BYTE_PREFIX = b'\xef'

MAINNET_SEGWIT_ADDRESS_PREFIX = 'bc'
TESTNET_SEGWIT_ADDRESS_PREFIX = 'tb'
BECH32M_CONST = 0x2bc830a3

SCRIPT_TYPES = {"P2PKH":        0,
                "P2SH":         1,
                "PUBKEY":       2,
                "NULL_DATA":    3,
                "MULTISIG":     4,
                "P2WPKH":       5,
                "P2WSH":        6,
                "NON_STANDARD": 7,
                "NULL_DATA_NON_STANDARD": 8,
                "V1_P2TR": 9
                }

SCRIPT_N_TYPES = {0: "P2PKH",
                  1: "P2SH",
                  2: "PUBKEY",
                  3: "NULL_DATA",
                  4: "MULTISIG",
                  5: "P2WPKH",
                  6: "P2WSH",
                  7: "NON_STANDARD",
                  8: "NULL_DATA_NON_STANDARD",
                  9: "V1_P2TR"
                }