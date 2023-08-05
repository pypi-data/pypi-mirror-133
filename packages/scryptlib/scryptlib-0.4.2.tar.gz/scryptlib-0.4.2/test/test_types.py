import pytest

from scryptlib.types import *


def test_type_bytes():
    b = Bytes('01')
    assert(b.hex == '0101')

    b = Bytes(b'\x01')
    assert(b.hex == '0101')

    # OP_PUSHDATA1
    b = Bytes('ff' * 100)
    assert(b.hex == '4c64' + 'ff' * 100)
    b = Bytes('ff' * 255)
    assert(b.hex == '4cff' + 'ff' * 255)

    # OP_PUSHDATA2
    b = Bytes('ff' * 256)
    assert(b.hex == '4d0001' + 'ff' * 256)
    b = Bytes('ff' * 65535)
    assert(b.hex == '4dffff' + 'ff' * 65535)

    # OP_PUSHDATA4
    b = Bytes('ff' * 65536)
    assert(b.hex == '4e00000100' + 'ff' * 65536)


def test_type_hashedmap():
    hm = HashedMap(Int, Int)
    hm.set(Int(3), Int(1))
    assert(hm.hex == '084fed08b978af4d7d196a7446a86b58009e636b611db16211b65a9aadff29c54bf5122f344554c53bde2ebb8cd2b7e3d1600ad631c385a5d7cce23c7785459a')
    hm.set(Int(5), Int(6))
    assert(hm.hex == 'e77b9a9ae9e30b0dbdb6f510a264ef9de781501d7b6b92ae89eb059c5ab743db67586e98fad27da0b9968bc039a1ef34c939b9b8e523a8bef89d478608c5ecf6084fed08b978af4d7d196a7446a86b58009e636b611db16211b65a9aadff29c54bf5122f344554c53bde2ebb8cd2b7e3d1600ad631c385a5d7cce23c7785459a')
    hm.set(0, 11)
    assert(hm.hex == 'e77b9a9ae9e30b0dbdb6f510a264ef9de781501d7b6b92ae89eb059c5ab743db67586e98fad27da0b9968bc039a1ef34c939b9b8e523a8bef89d478608c5ecf6084fed08b978af4d7d196a7446a86b58009e636b611db16211b65a9aadff29c54bf5122f344554c53bde2ebb8cd2b7e3d1600ad631c385a5d7cce23c7785459ae3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855e7cf46a078fed4fafd0b5e3aff144802b853f8ae459a4f0c14add3314b7cc3a6')
    hm.set(Int(1), Int(5))
    assert(hm.hex == 'e77b9a9ae9e30b0dbdb6f510a264ef9de781501d7b6b92ae89eb059c5ab743db67586e98fad27da0b9968bc039a1ef34c939b9b8e523a8bef89d478608c5ecf6084fed08b978af4d7d196a7446a86b58009e636b611db16211b65a9aadff29c54bf5122f344554c53bde2ebb8cd2b7e3d1600ad631c385a5d7cce23c7785459a4bf5122f344554c53bde2ebb8cd2b7e3d1600ad631c385a5d7cce23c7785459ae77b9a9ae9e30b0dbdb6f510a264ef9de781501d7b6b92ae89eb059c5ab743dbe3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855e7cf46a078fed4fafd0b5e3aff144802b853f8ae459a4f0c14add3314b7cc3a6')

    hm.delete(Int(1))
    hm.delete(Int(0))
    assert(hm.hex == 'e77b9a9ae9e30b0dbdb6f510a264ef9de781501d7b6b92ae89eb059c5ab743db67586e98fad27da0b9968bc039a1ef34c939b9b8e523a8bef89d478608c5ecf6084fed08b978af4d7d196a7446a86b58009e636b611db16211b65a9aadff29c54bf5122f344554c53bde2ebb8cd2b7e3d1600ad631c385a5d7cce23c7785459a')

    hm = HashedMap(Bytes, Int)

    with pytest.raises(AssertionError):
        hm.set(Int(0), Int(1))

    hm.set(Bytes('1234'), Int(11))


def test_type_hashedset():
    hs = HashedSet(Int)
    hs.add(3)
    assert(hs.hex == '084fed08b978af4d7d196a7446a86b58009e636b611db16211b65a9aadff29c5')
    hs.add(Int(5))
    assert(hs.hex == 'e77b9a9ae9e30b0dbdb6f510a264ef9de781501d7b6b92ae89eb059c5ab743db084fed08b978af4d7d196a7446a86b58009e636b611db16211b65a9aadff29c5')
    hs.add(0)
    assert(hs.hex == 'e77b9a9ae9e30b0dbdb6f510a264ef9de781501d7b6b92ae89eb059c5ab743db084fed08b978af4d7d196a7446a86b58009e636b611db16211b65a9aadff29c5e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855')
    hs.add(Int(1))
    assert(hs.hex == 'e77b9a9ae9e30b0dbdb6f510a264ef9de781501d7b6b92ae89eb059c5ab743db084fed08b978af4d7d196a7446a86b58009e636b611db16211b65a9aadff29c54bf5122f344554c53bde2ebb8cd2b7e3d1600ad631c385a5d7cce23c7785459ae3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855')

    hs.delete(Int(1))
    hs.delete(Int(0))
    assert(hs.hex == 'e77b9a9ae9e30b0dbdb6f510a264ef9de781501d7b6b92ae89eb059c5ab743db084fed08b978af4d7d196a7446a86b58009e636b611db16211b65a9aadff29c5')


