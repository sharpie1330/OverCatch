import copy
import numpy as np
from pandas import Series


class Dist:

    @staticmethod
    def init_oc(nc):
        oc = {}
        for i in range(nc):
            oc[i] = []
        return oc

    @staticmethod
    def get_distance(dist_file_path, nc=13):
        # init
        oc = Dist.init_oc(nc)
        oc_frame = Dist.init_oc(nc)
        oc_dist = Dist.init_oc(nc)
        oc_conf = Dist.init_oc(nc)

        with open(f'{dist_file_path}', 'r') as f:
            contents = f.readlines()
            for line in contents:
                frame, cls, dist, conf = line.split()
                oc[int(cls)].append((int(frame), float(dist), float(conf)))
                oc_frame[int(cls)].append(int(frame))
                oc_dist[int(cls)].append(float(dist))
                oc_conf[int(cls)].append(float(conf))

        return oc, oc_frame, oc_dist, oc_conf

    @staticmethod
    def get_ks_list(oc):
        # init
        ks_cnt = 0
        ks_frame_1st, ks_frame_2rd = 0, 0
        # 킬사인 기준 -> 거리가 100 미만일 때 / conf 가 0.2 이상일 때
        # 그 외 다른 기준은 현재 고려 하지 않음.
        ks_list = []
        for elem in oc[12]:  # 12 -> kill-sign
            if elem[1] < 100 and elem[2] >= 0.2:  # 거리가 100보다 작고, conf가 0.2 이상일 때
                if ks_cnt == 0:  # 첫 번째 ks frame
                    ks_frame = elem[0]
                    ks_frame_1st = ks_frame
                    ks_list.append(ks_frame)
                    ks_cnt += 1
                else:
                    ks_frame_2rd = elem[0]
                    # 이전 ks_frame_ex와 바로 다음 ks_frame_ex 사이의 차가 10 이상일 때
                    if ks_frame_2rd - ks_frame_1st > 10:
                        ks_frame = ks_frame_2rd
                        ks_list.append(ks_frame)
                    ks_frame_1st = ks_frame_2rd
        return ks_list

    @staticmethod
    def get_target(oc, oc_frame, oc_dist, oc_conf, ks_list, nc=13):
        ks_result = {}  # 킬사인 프레임 별 타겟
        ks_result_frame = {}
        ks_dist_diff = {}
        ks_vanilla = {}

        for frame in ks_list:
            temp = Dist.init_oc(nc)
            vanilla = Dist.init_oc(nc)
            killed_std_30 = {}
            killed_std_7 = {}
            killed_mean_30 = {}
            killed_mean_7 = {}
            wp = {}
            interp = {}
            del_outlier = {}
            dummy = {}

            # 킬사인 앞 30프레임 찾기, 중복 프레임은 conf값 더 높은 것으로 저장
            for cls in range(nc - 1):
                if frame >= 30:
                    for n in reversed(range(30)):
                        index_list = list(filter(lambda x: oc_frame[cls][x] == frame - n,
                                                 range(len(oc_frame[cls]))))
                        if len(index_list) > 0:
                            s = dict()
                            for i in index_list:
                                s[i] = oc_conf[cls][i]
                            s = sorted(s.items(), key=lambda item: item[1], reverse=True)
                            index = s[0][0]
                            temp[cls].append(oc_dist[cls][index])
                            vanilla[cls].append(oc_dist[cls][index])
                        else:
                            temp[cls].append(np.nan)
                            vanilla[cls].append(np.nan)

            # vanilla 이상치 제거
            # for cls in range(nc-1):
            #     if not vanilla[cls].count(np.nan) == 30:
            #         Q1 = np.percentile(np.array(Series(vanilla[cls]).dropna().tolist()), 25)
            #         Q3 = np.percentile(np.array(Series(vanilla[cls]).dropna().tolist()), 75)
            #         IQR = Q3 - Q1
            #         v_result = list(((Q1 - 1.5 * IQR <= vanilla[cls]) & (Q3 + 1.5 * IQR >= vanilla[cls])) | numpy.isnan(vanilla[cls]))
            #         v_result_filtered = list()
            #         v_not_true_index = list(filter(lambda x: v_result[x] != 1.0, range(len(v_result))))
            #         for index in range(len(vanilla[cls])):
            #             if not v_not_true_index.count(index) > 0:
            #                 v_result_filtered.append(vanilla[cls][index])
            #         vanilla[cls] = copy.deepcopy(v_result_filtered)
            #     else:
            #         vanilla[cls] = list()

            # 30프레임/ 7프레임 별 표준 편차, 평균 계산 - 7프레임 이상 존재할 때
            for cls in range(nc - 1):
                # cls 별 30프레임 데이터 임시 저장
                dummy[cls] = copy.deepcopy(temp[cls])
                # weight point 값 초기화
                wp[cls] = 0
                # 30프레임이 전부 nan인 게 아닐 때 -> 앞 뒤 보간되지 않는 nan 값 삭제
                if dummy[cls].count(np.nan) < 30:
                    if np.isnan(temp[cls][-1]):
                        while np.isnan(temp[cls][-1]):
                            del temp[cls][-1]
                    if np.isnan(temp[cls][0]):
                        while np.isnan(temp[cls][0]):
                            del temp[cls][0]
                # 전부 nan이면 빈 리스트로 만들기
                else:
                    temp[cls] = list()
                # 선형 보간
                interp[cls] = list(Series(temp[cls], dtype=float).interpolate())
                # 킬 사인 이전 7프레임 임시 저장
                temp_list = dummy[cls][-7:]
                # 보간한 데이터의 길이가 0보다 클 때(빈 리스트가 아닐 때)
                if len(interp[cls]) > 0:
                    # 4원수값을 활용, 이상치 제거
                    Q1 = np.percentile(np.array(interp[cls]), 25)
                    Q3 = np.percentile(np.array(interp[cls]), 75)
                    IQR = Q3 - Q1
                    result = list((Q1 - 1.5 * IQR <= interp[cls]) & (Q3 + 1.5 * IQR >= interp[cls]))
                    result_filtered = list()
                    not_true_index = list(filter(lambda x: result[x] != 1.0, range(len(result))))
                    for index in range(len(interp[cls])):
                        if not not_true_index.count(index) > 0:
                            result_filtered.append(interp[cls][index])
                    # 이상치 제거한 값으로 del_outlier 딕셔너리에 저장
                    del_outlier[cls] = copy.deepcopy(result_filtered)
                else:
                    # 보간할 값이 없으면(nan만 있는 리스트) 빈 리스트 저장
                    del_outlier[cls] = list()
                    # dist_diff[cls] = list()
                # 만약 nan이 아닌 값이 3개 이상 포함되어 있을 경우 - del_outlier 말고 interp로
                # (len(interp[cls] >= 3과 동일할 것으로 추정되나 오류 예방)
                if np.count_nonzero(~np.isnan(interp[cls])) >= 3:
                    # 해당 cls의 wp 값을 리스트의 길이만큼 ++
                    wp[cls] = len(interp[cls])
                    # 전체 보간, 이상치 제거된 리스트의 표준편차, 평균 구하기
                    killed_std_30[cls] = np.std(del_outlier[cls])
                    killed_mean_30[cls] = np.mean(del_outlier[cls])
                    # if len(del_outlier[cls]) > 7:
                    #     killed_std_7[cls] = np.std(del_outlier[cls][-7:])
                    #     killed_mean_7[cls] = np.mean(del_outlier[cls][-7:])
                    # 위에서 임시저장한 킬사인 앞 7프레임 데이터에 nan값이 포함되어 있다면 전부 제거
                    while temp_list.count(np.nan) > 0:
                        del temp_list[temp_list.index(np.nan)]
                    # temp_list가 빈 리스트가 아니면
                    if len(temp_list) > 0:
                        # 킬사인 앞 7프레임의 표준편차, 평균 값 구하기
                        killed_std_7[cls] = np.std(temp_list)
                        killed_mean_7[cls] = np.mean(temp_list)

            # 정렬 - 내림 차순 -> 표준 편차가 작을 수록 높은 점수, 평균이 작을 수록 높은 점수
            killed_std_30 = sorted({k: v for k, v in killed_std_30.items() if not np.isnan(v) and v != 0}.items(),
                                   key=lambda item: item[1], reverse=True)
            killed_std_7 = sorted({k: v for k, v in killed_std_7.items() if not np.isnan(v) and v != 0}.items(),
                                  key=lambda item: item[1], reverse=True)
            killed_mean_30 = sorted({k: v for k, v in killed_mean_30.items() if not np.isnan(v) and v != 0}.items(),
                                    key=lambda item: item[1], reverse=True)
            killed_mean_7 = sorted({k: v for k, v in killed_mean_7.items() if not np.isnan(v) and v != 0}.items(),
                                   key=lambda item: item[1], reverse=True)

            # 가중치 더하기
            # 30프레임 표준 편차: 인덱스 * 2 / 10프레임 표준 편차: 인덱스 * 3
            # 30프레임 평균: 인덱스 * 5 / 10프레임 평균: 인덱스 * 6
            for n in killed_std_30:
                if not len(killed_std_30) <= 1:
                    wp[n[0]] += 2 * (killed_std_30.index(n) + 1)

            for n in killed_std_7:
                if not len(killed_std_7) <= 1:
                    wp[n[0]] += 3 * (killed_std_7.index(n) + 1)

            for n in killed_mean_30:
                if not len(killed_mean_30) <= 1:
                    wp[n[0]] += 5 * (killed_mean_30.index(n) + 1)

            for n in killed_mean_7:
                if not len(killed_mean_7) <= 1:
                    wp[n[0]] += 6 * (killed_mean_7.index(n) + 1)

            # nan이 아닌 값 개수 * 3을 wp에 더해줌
            # 빈도수 파악
            for cls in range(nc - 1):
                wp[cls] += 3 * np.count_nonzero(~np.isnan(dummy[cls]))

            # 사정거리 250 이내일 때 조준했다고 가정, 그 평균이 작을수록 타겟이라고 판단
            cls_temp = {}
            minus_temp = {}
            for cls in range(nc - 1):
                cnt = 0
                t = list()
                # nan이 제거되고 보간된 리스트에 대해서, 값이 nan이 아니고 뒤에서부터 7개 요소에서 250 미만의 값 개수 count
                # 리스트 자체 길이가 3 이상인지 확인, 리스트 길이 자체가 7이 안되면 리스트의 길이만큼만, 아니면 7개로 제한
                if len(interp[cls]) >= 3:
                    if len(interp[cls]) < 7:
                        tp = interp[cls][-len(interp[cls]):]
                    else:
                        tp = interp[cls][-7:]
                    for element in tp:
                        if not np.isnan(element):
                            if element < 200:
                                cnt += 1
                            t.append(element)
                # 그 개수가 0보다 크고, 그 중에서 nan이 아닌 값이 3개 이상이면
                if cnt > 0 and np.count_nonzero(~np.isnan(tp)) >= 3:
                    # 그리고 평균이 250 미만이면 평균값 저장
                    if np.mean(t) < 250:
                        cls_temp[cls] = np.mean(t)
                    # 그 이외의 경우 minus_temp 딕셔너리에 저장(가중치 빼기 위함)
                    elif np.mean(t) > 550:
                        wp[cls] = 0
                    else:
                        minus_temp[cls] = np.mean(t)
                else:
                    wp[cls] = 0
            # 큰 순으로 나열, 작을수록 더 많은 가중치(인덱스 값 * 7)를 더하도록
            cls_temp = sorted(cls_temp.items(), key=lambda item: item[1], reverse=True)
            for n in cls_temp:
                wp[n[0]] += 7 * (cls_temp.index(n) + 1)
            # 작은 순으로 나열, 클수록 더 많은 가중치 빼도록!
            minus_temp = sorted(minus_temp.items(), key=lambda item: item[1])
            for n in minus_temp:
                wp[n[0]] -= 7 * (minus_temp.index(n) + 1)

            # weightpoints dict를 값을 기준으로 정렬 -> wp가 클수록 앞으로 정렬
            wp = sorted(wp.items(), key=lambda item: item[1], reverse=True)

            # wp값이 0보다 크면 그대로, 아니면 -1 저장, 상위 두 cls 값이 같을 때도 -1 -> -1은 타겟을 찾지 못했음을 의미
            if wp[0][1] == wp[1][1]:
                ks_result[frame] = -1
            if wp[0][1] > 0:
                ks_result[frame] = wp[0][0]
            else:
                ks_result[frame] = -1

            if not ks_result[frame] == -1:
                ks_result_frame[frame] = del_outlier[ks_result[frame]]
                ks_vanilla[frame] = copy.deepcopy(vanilla[ks_result[frame]])   #edit
                # 거리의 차 dist_diff 딕셔너리에 저장
                dod = list()
                if len(del_outlier[ks_result[frame]]) > 1:  # 리스트 길이가 1보다 클 때만(1이거나 0일 때는 생략)
                    for i in range(len(del_outlier[ks_result[frame]]) - 1):
                        dod.append(abs(del_outlier[ks_result[frame]][i + 1] - del_outlier[ks_result[frame]][i]))
                ks_dist_diff[frame] = copy.deepcopy(dod)
            else:
                ks_result_frame[frame] = -1
                ks_vanilla[frame] = -1  #edit
                ks_dist_diff[frame] = -1

        return ks_result, ks_result_frame, ks_dist_diff, ks_vanilla

    @staticmethod
    def get_dict(dist_txt_path):

        oc_dict, frame_dict, dist_dict, conf_dict = Dist.get_distance(dist_file_path=dist_txt_path, nc=13)
        ks_list = Dist.get_ks_list(oc_dict)

        ks_result, ks_result_frame, ks_dist_diff, ks_vanilla = \
            Dist.get_target(oc_dict, frame_dict, dist_dict, conf_dict, ks_list, nc=13)
        # print(ks_result)
        # target_list = ['ANA', 'BASTION', 'CASSIDY', 'LUCIO', 'MEI',
        #                'REAPER', 'ROADHOG', 'SOLDIER-76', 'SOMBRA', 'TORBJORN',
        #                'ZARYA', 'ZENYATA', 'kill-sign']
        #
        # for key, value in ks_result.items():
        #     if ks_result[key] == -1:
        #         ks_result[key] = 'NOTFOUND'
        #     else:
        #         ks_result[key] = target_list[value]
        #
        # print(ks_result)
        # print(ks_result_frame)
        return ks_result, ks_result_frame, ks_dist_diff, ks_vanilla

