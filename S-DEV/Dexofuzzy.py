import dexofuzzy

#dex파일이 해시값을 계산하는 함수. 
def calculate_dex_hash(apk_file_path):
    # hash_from_file 함수를 사용하여 Dex 파일의 해시를 계산함.
    dex_hash = dexofuzzy.hash_from_file(apk_file_path) #apk파일의 해시값을 계산함. 리턴값은 계산된 Dex 파일 해시 값(str)이 나옴.
    return dex_hash

#두 개의 APK 파일의 Dex 파일 해시를 비교하는 함수
def compare_dex_hashes(apk_file_path1, apk_file_path2):
    # sample1.apk의 Dex 파일 해시 계산함
    dex_hash1 = calculate_dex_hash(apk_file_path1)

    # sample2.apk의 Dex 파일 해시 계산함
    dex_hash2 = calculate_dex_hash(apk_file_path2)

    # 계산된 Dex 파일 해시를 출력함.
    print(f"Dex Hash for {apk_file_path1}: {dex_hash1}")
    print(f"Dex Hash for {apk_file_path2}: {dex_hash2}")

    # 두 해시를 비교함.
    similarity = dexofuzzy.compare(dex_hash1, dex_hash2) #두 해시간의 유사도를 계산해서 백분율로 반환함. 반환값은 0에서 100까지의 정수.
    print(f"Similarity between Dex Hashes: {similarity:.2%}")

if __name__ == "__main__":
    # 비교할 APK 파일 경로 설정
    apk_file_path1 = "sample1.apk"
    apk_file_path2 = "sample2.apk"

    # Dex 파일 해시 비교
    compare_dex_hashes(apk_file_path1, apk_file_path2)
