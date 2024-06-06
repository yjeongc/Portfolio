import json

# API에 대한 위협 가중치를 리턴하는 함수.
def apply_threat_score(api_name):
    # API에 대한 위협 가중치를 정의한 딕셔너리.
    threat_scores = {
        'getDeviceId': 4, 'getSimSerialNumber': 6, 'getSubscriberId': 5,
        'sendTextMessage': 9, 'getMessageBody': 9, 'delete': 3, 'createFromPdu': 3,
        'getLineNumber': 6, 'getRunningTasks': 7, 'getSimOperator': 6,
        'getSimOperatorName': 6, 'connect': 3, 'notify': 3,
        'killBackgroundProcesses': 3, 'registerContentObserver': 3,
        'encode': 3, 'getURL': 3,
    }
    # API 이름에 해당하는 위협 가중치를 반환함. 없으면 기본값 1 반환
    return threat_scores.get(api_name, 1)

def calculate_category_score(category_counts):
    # 각 카테고리에 대한 API 점수 합이 100을 넘지 않도록 하는 함수
    return {category: min(sum(api_count.values()), 100) for category, api_count in category_counts.items()}

def calculate_threat_scores(category_counts):
    # 카테고리별 API 카운트에 위협 가중치를 곱하는 함수
    for category, api_count in category_counts.items():
        for api, count in api_count.items():
            # apply_threat_score 함수를 통해 API 이름에 맞는 위협 가중치를 가져옴
            threat_score = apply_threat_score(api)
            # 기존 API 호출 횟수에 위협 가중치를 곱하여 category_counts 딕셔너리에 반영함.
            category_counts[category][api] *= threat_score
    return category_counts

def main(json_file_path):
    # Json 파일 경로를 직접 설정함.

    with open(json_file_path, 'r') as json_file:
        # JSON 파일을 읽어서 데이터를 json_data에 저장함.
        json_data = json.load(json_file)

    # 각 카테고리별로 API 목록을 정의함.
    api_categories = {
        'Privacy': ['getDeviceId', 'getSimSerialNumber', 'getSubscriberId'],
        'SMS': ['sendTextMessage', 'getMessageBody'],
        'Linux': ['su', 'du', 'gzip', 'mkdir', 'chmod', 'chown', 'cp'],
        'FileAccess': ['delete', 'createFromPdu'],
        'Device': ['getLineNumber', 'getLatitude', 'getLongitude', 'getRunningTasks',
                   'getSimOperator', 'getSimOperatorName', 'connect', 'notify',
                   'killBackgroundProcesses', 'registerContentObserver'],
        'Network': ['encode', 'getURL']
    }

    # 각 카테고리에 속하는 API들의 호출 횟수를 0으로 초기화함.
    category_counts = {category: {api: 0 for api in apis} for category, apis in api_categories.items()}

    # API가 호출될 때마다 API를 카테고리에 매핑하여 카운트를 1씩 증가시킴.
    for class_info in json_data['Classes']:
        methods = class_info.get('method', [])
        for method in methods:
            api_name = method.get('name')
            for category, apis in api_categories.items():
                if api_name in apis:
                    category_counts[category][api_name] += 1

    # 각 API의 이름과 호출 횟수를 딕셔너리에 담아서 출력함 (호출 횟수가 0보다 클 때만 출력)
    api_counts_dict = {category: {api: count for api, count in api_count.items() if count > 0} for category, api_count in category_counts.items()}

    # 위협 점수를 적용한 각 API의 점수를 계산함
    modified_category_counts = calculate_threat_scores(category_counts)

    # 각 카테고리에 대한 총 점수를 계산함
    category_scores = calculate_category_score(modified_category_counts)

    # 반환값 api_counts_dict과 category_scores을 튜플로 묶어서 반환
    return api_counts_dict, category_scores
