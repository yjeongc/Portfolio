import dexofuzzy

#dex������ �ؽð��� ����ϴ� �Լ�. 
def calculate_dex_hash(apk_file_path):
    # hash_from_file �Լ��� ����Ͽ� Dex ������ �ؽø� �����.
    dex_hash = dexofuzzy.hash_from_file(apk_file_path) #apk������ �ؽð��� �����. ���ϰ��� ���� Dex ���� �ؽ� ��(str)�� ����.
    return dex_hash

#�� ���� APK ������ Dex ���� �ؽø� ���ϴ� �Լ�
def compare_dex_hashes(apk_file_path1, apk_file_path2):
    # sample1.apk�� Dex ���� �ؽ� �����
    dex_hash1 = calculate_dex_hash(apk_file_path1)

    # sample2.apk�� Dex ���� �ؽ� �����
    dex_hash2 = calculate_dex_hash(apk_file_path2)

    # ���� Dex ���� �ؽø� �����.
    print(f"Dex Hash for {apk_file_path1}: {dex_hash1}")
    print(f"Dex Hash for {apk_file_path2}: {dex_hash2}")

    # �� �ؽø� ����.
    similarity = dexofuzzy.compare(dex_hash1, dex_hash2) #�� �ؽð��� ���絵�� ����ؼ� ������� ��ȯ��. ��ȯ���� 0���� 100������ ����.
    print(f"Similarity between Dex Hashes: {similarity:.2%}")

if __name__ == "__main__":
    # ���� APK ���� ��� ����
    apk_file_path1 = "sample1.apk"
    apk_file_path2 = "sample2.apk"

    # Dex ���� �ؽ� ��
    compare_dex_hashes(apk_file_path1, apk_file_path2)
