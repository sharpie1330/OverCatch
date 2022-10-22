import time
from dist import Dist

ID = 0
first = 0


def get_csv(is_hack, video_id, dist_txt_path):
    global ID, first
    start = time.time()
    ks_result, ks_result_frame, ks_dist_diff, ks_vanilla = Dist.get_dict(dist_txt_path)
    info_file = open('C:/WatchHack/info.csv', 'a')
    if first == 0:
        info_file.write('id,video_id,isHack,ks_frame,target\n')
        first += 1
    for k, v in ks_result.items():
        if not v == -1:
            info_file.write(str(ID) + ',' + str(video_id) + ','
                            + str(is_hack) + ',' + str(k) + ','
                            + str(v) + '\n')
            dist_file = open('C:/WatchHack/dist_data/distance_{}.csv'.format(ID), 'w')
            dist_diff_file = open('C:/WatchHack/dist_diff_data/dist_diff_{}.csv'.format(ID), 'w')
            dist_vanilla_file = open('C:/WatchHack/dist_vanilla_data/dist_vanilla_{}.csv'.format(ID), 'w')
            dist_file.write('distance\n')
            dist_diff_file.write('dist_diff\n')
            dist_vanilla_file.write('dist_vanilla\n')
            for n in range(len(ks_result_frame[k])):
                dist_file.write(str(ks_result_frame[k][n]) + '\n')
            for n in range(len(ks_dist_diff[k])):
                dist_diff_file.write(str(ks_dist_diff[k][n]) + '\n')
            for n in range(len(ks_vanilla[k])):
                dist_vanilla_file.write(str(ks_vanilla[k][n]) + '\n')
            ID += 1
        else:
            print('NOTFOUND')
    end = time.time()
    print('total', '%.2fs' % (end - start), 'elapsed.')


# gen, hack 데이터 35개 기준

# id, first -> 0으로 변경 후 실행
for i in range(35):
    get_csv(0, i+1, 'C:/WatchHack/dist30/gen_{}_dist.txt'.format(i+1))

# id -> 994, first -> 1로 변경 후 실행
# for i in range(35):
#     get_csv(1, i+1, 'C:/WatchHack/dist30/hack_{}_dist.txt'.format(i+1))
