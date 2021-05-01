import datetime
import hashlib
lst_files = [r"/home/martin/privat/Martin_substitute.html.pgp",
             r"/home/martin/privat/Christmas_2020/L/2000284-kvittering-guccadk.pdf",
             r"/home/martin/privat/Christmas_2020/L/Til bestilling - Bang & Olufsen Hellerup · Rødovre.7z"]
num_iter = 999

def hashafile(str_full_path, algorithm='md5', max_chunks=0):
    if algorithm == 'sha1':
        hash_alg = hashlib.sha1()  # Frequently used, speed access
    elif algorithm in hashlib.algorithms_available:
        hash_alg = hashlib.new(algorithm)
    else:
        hash_alg = hashlib.md5()  # It's our default
    with open(str_full_path, "rb") as f:
        num_chunk = 0
        for chunk in iter(lambda: f.read(65536), b""):  # 64k buffer
            hash_alg.update(chunk)
            num_chunk += 1
            if max_chunks > 0 and num_chunk >= max_chunks:
                return hash_alg.hexdigest()
    return hash_alg.hexdigest()


for algo in hashlib.algorithms_available:
    if algo not in ["shake_128", "shake_256"]:
        dtt_beg = datetime.datetime.now()
        for str_ffn in lst_files:
            for n in range(num_iter):
                hash = hashafile(str_ffn, algo)
        dur_a = datetime.datetime.now() - dtt_beg
        print(f"algo: {algo}, dura: {dur_a}")
        #print(f"      hash: {hashafile(str_ffn, algo)}")





# ---
# algo: sha1, dura: 0:00:00.799011
# algo: sha1, dura: 0:00:00.821846
# algo: sha1, dura: 0:00:00.851415
# algo: sha224, dura: 0:00:00.993969
# algo: sha224, dura: 0:00:00.996233
#
#
# algo: blake2b, dura: 0:00:01.605820
# algo: blake2b, dura: 0:00:01.650850
# algo: blake2b, dura: 0:00:01.719190
# algo: md4, dura: 0:00:01.101630
# algo: md4, dura: 0:00:01.103751
# algo: md4, dura: 0:00:01.207325
# algo: md5, dura: 0:00:01.703324
# algo: md5, dura: 0:00:01.714132
# algo: md5, dura: 0:00:01.715611
# algo: sha224, dura: 0:00:01.035845
# algo: sha256, dura: 0:00:01.002259
# algo: sha256, dura: 0:00:01.095818
# algo: sha256, dura: 0:00:01.138643
# algo: sha384, dura: 0:00:01.973516
# algo: sha512, dura: 0:00:01.949959
# algo: sha512, dura: 0:00:01.980224
# algo: sha512_224, dura: 0:00:01.962905
# algo: sha512_224, dura: 0:00:01.980453
# algo: sha512_256, dura: 0:00:01.944438
#
# algo: whirlpool, dura: 0:00:06.915660
# algo: sm3, dura: 0:00:04.726817
# algo: ripemd160, dura: 0:00:04.072563
# algo: md5-sha1, dura: 0:00:02.419754
# algo: sha3_512, dura: 0:00:06.040042
# algo: blake2s, dura: 0:00:02.466029
# algo: sha3_384, dura: 0:00:04.224057
# algo: sha3_256, dura: 0:00:03.475361
# algo: sha3_224, dura: 0:00:03.298201
# algo: sha512, dura: 0:00:02.337362
# algo: sha384, dura: 0:00:02.254069
# algo: sha512_256, dura: 0:00:02.182687
# algo: sha3_256, dura: 0:00:03.229244
# algo: whirlpool, dura: 0:00:06.854681
# algo: sha3_384, dura: 0:00:04.120698
# algo: sha3_512, dura: 0:00:05.876200
# algo: ripemd160, dura: 0:00:04.044311
# algo: md5-sha1, dura: 0:00:02.424719
# algo: sha3_224, dura: 0:00:03.051560
# algo: blake2s, dura: 0:00:02.463013
# algo: sm3, dura: 0:00:04.718836
# algo: sm3, dura: 0:00:04.894519
# algo: sha512_256, dura: 0:00:02.131273
# algo: sha3_256, dura: 0:00:03.200890
# algo: sha512_224, dura: 0:00:02.024940
# algo: blake2s, dura: 0:00:02.462740
# algo: md5-sha1, dura: 0:00:02.492798
# algo: sha384, dura: 0:00:02.011916
# algo: sha3_384, dura: 0:00:04.167702
# algo: sha3_224, dura: 0:00:03.152619
# algo: whirlpool, dura: 0:00:07.290639
# algo: ripemd160, dura: 0:00:04.318322
# algo: sha3_512, dura: 0:00:05.942645
